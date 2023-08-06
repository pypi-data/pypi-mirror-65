# -*- coding: UTF-8 -*
from __future__ import print_function

import hashlib
import json
import random
import time
import logging

__version__ = "1.0.6"


class UniApiBase(object):
    apiurl = None
    appid = None
    appkey = None

    @classmethod
    def md5(clz, src):
        if type(src) == type(u''):
            src = src.encode('utf8')
        return hashlib.md5(src).hexdigest()

    @classmethod
    def md5sign(clz, data, key):
        l = ['%s=%s' % (k, v) for (k, v) in data.items() if v]
        l.sort()
        s = '&'.join(l)
        s = '%s&key=%s' % (s, key)
        ms = UniApiBase.md5(s).upper()
        return ms

    @classmethod
    def nonce_str(clz):
        return UniApiBase.md5('%s%s' % (time.time(), random.randint(100000, 999999)))[0:24]

    def doapi(self, apiname, data):
        import requests
        if isinstance(data, dict):
            if 'noncestr' not in data:
                data['noncestr'] = UniApiBase.nonce_str()
            if 'sign' not in data and self.appkey:
                data['sign'] = UniApiBase.md5sign(data, self.appkey)
                #             data = json.dumps(data)
        r = requests.request('post', url='%s%s' % (self.apiurl, apiname), data=data)
        r.raise_for_status()
        res = json.loads(r.content)
        return res


class IRApi(UniApiBase):
    def __init__(self, appid, appkey, apiurl=None, *args, **kwargs):
        object.__init__(self, *args, **kwargs)
        self.appid = appid
        self.appkey = appkey
        if apiurl:
            self.apiurl = apiurl
        if not self.apiurl:
            raise ValueError("Has not apiurl")

    def doapi(self, apiname, data):

        if isinstance(data, dict):
            if 'appid' not in data:
                data['appid'] = self.appid
        return UniApiBase.doapi(self, apiname, data)

    def sendCode(self, phone, code):
        return self.doapi('sendSMSCode', {'phones': phone, 'code': code})['code'] == 0

    def sendNoti(self, phones, content, sign_name='', template_code=''):
        if type(phones) == list:
            phones = ','.join(phones)
        return self.doapi('sendSMSNoti', {'phones': phones, 'content': content, 'sign_name': sign_name, 'template_code': template_code})['code'] == 0

    def sendWS(self, data, tag, filterdic=None):
        return self.doapi('sendWS', {'datajson': json.dumps(data), 'tag': tag, 'filterjson': json.dumps(filterdic) if filterdic else None})

    def transLang(self, **param):
        return self.doapi('transLang', param)


def main():
    import argparse
    try:
        import urlparse as parse
    except:
        from urllib import parse

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-u', '--apiurl', help='the API base url', required=True)
    parser.add_argument('-a', '--appid', help='the APPID', required=False)
    parser.add_argument('-k', '--appkey', help='the APPKEY', required=False)
    parser.add_argument('-i', '--apiname', help='the api name', required=True)
    parser.add_argument('-d', '--data', help='the json data')
    args = parser.parse_args()

    api = IRApi(appid=args.appid, appkey=args.appkey, apiurl=args.apiurl)
    data = args.data
    param = parse.parse_qs(data)
    data = {
        k: v[0] for k, v in param.items()
    }
    for k in data:
        v = data[k]
        if v == 'STDIN':
            import sys
            nv = sys.stdin.read()
            if type(nv) != type(''):
                nv = nv.decode()
            data[k] = nv.strip()
    r = api.doapi(args.apiname, data=data)

    print(json.dumps(r, ensure_ascii=False))
    if r.get('msg'):
        print('\033[41;30m%s\033[0m' % (r['msg']))
    exit(r.get('code'))


class IRApiLoggingHandler(logging.Handler):
    format_keys = None

    def __init__(self, apiurl, appid, apiname, appkey=None, apidata=None, debug=False, enable=True):
        self.api = IRApi(appid=appid, appkey=appkey, apiurl=apiurl)
        self.apiname = apiname
        self.apidata = apidata
        self.debug = debug
        self.enable = enable
        logging.Handler.__init__(self)
        if apidata:
            import re
            format_keys = set()
            if isinstance(apidata, dict):
                for k, v in apidata.items():
                    for r in re.findall('\\${(\S+?)}', v):
                        format_keys.add((r, k), )
            else:
                # string
                for r in re.findall('\\${(\S+?)}', apidata):
                    format_keys.add(r)
            self.format_keys = format_keys
        else:
            self.format_keys = None
        self._datas = None
        self._running = True

    def _add_data_task(self, data):
        if self._datas == None:
            try:
                from queue import Queue
            except:
                from Queue import Queue
            self._datas = Queue(maxsize=-1)

            def _run():
                while self._running:
                    d = self._datas.get()
                    count = 3
                    while d and count:
                        count -= 1
                        try:
                            if self.debug:
                                print('REQ', self.apiname, d)
                            r = self.api.doapi(self.apiname, data=d)
                            if self.debug:
                                print('RET', r)
                            break
                        except:
                            import time
                            time.sleep(3)

            import threading
            self._worker = threading.Thread(target=_run)
            self._worker.setDaemon(True)
            self._worker.start()
        self._datas.put(data)
        self._datas.empty()

    def emit(self, record):
        if not self.enable:
            return
        import datetime
        try:
            request = record.request
        except Exception:
            request = None
        cxt = {
            'request': request.META.get('REMOTE_ADDR') if request else '',
            'subject': record.getMessage(),
            'level': record.levelname,
            'message': self.format(record),
            'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        if self.apidata:
            if isinstance(self.apidata, dict):
                data = self.apidata.copy()
                for r, k in self.format_keys:
                    data[k] = data[k].replace('${%s}' % r, cxt.get(r, ''))
            else:
                # string
                data = self.apidata
                for r in self.format_keys:
                    data = data.replace('${%s}' % r, cxt.get(r, ''))
        else:
            data = None
        if data:
            self._add_data_task(data)

    def close(self):
        self._running = False
        if self._datas != None:
            self._datas.put(None)


if __name__ == '__main__':
    main()
