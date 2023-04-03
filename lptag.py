import datetime
import json
import random
# print(str(abs(round(9999999999*random.random()))))

import requests


class Lptag():
    def __init__(self):
        self.session = requests.session()
        self.session.proxies.update({'http': 'http://user-maximcrawl:cokeISit@gate.dc.smartproxy.com:20000',
                                     'https': 'http://user-maximcrawl:cokeISit@gate.dc.smartproxy.com:20000'})
        self.headers = {
            'accept': "*/*",
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': "en-US,en;q=0.9",
            'connection': 'keep-alive',
            'referer': 'https://www.answerfinancial.com/',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "macOS",
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.0.15'
        }

    def start_session(self, customer_id, ptitle, purl):
        s = str(round(random.random() * 99999)) + "x" + str(round(random.random() * 99999))
        self.tid = abs(round(9999999999 * random.random()))
        self.pid = abs(round(9999999999 * random.random()))
        d = {'cb':f'lpCb{s}',
             't':'sp',
             'ts':f"{int(datetime.datetime.now().timestamp() * 1000)}",
             'pid':self.pid,
             'tid':self.tid,
             'pt':ptitle,
             'u':purl,
             'df':'0',
             'os':'1',
             'sdes':[{"type":"ctmrinfo","info":{"customerId":f'{customer_id}'}}]}
        df = f"""https://va.v.liveperson.net/api/js/48853463?&cb={d['cb']}&t={d['t']}&ts={d['ts']}&pid={d['pid']}&tid={d['tid']}&pt=Compare%20car%20insurance%20quotes%2C%20buy%20%26%20save%20%7C%20Answer%20Financial&u=https%3A%2F%2F{d['u']}%2F&df={d['df']}&os={d['os']}&sdes=%5B%7B%22type%22%3A%22ctmrinfo%22%2C%22info%22%3A%7B%22customerId%22%3A%22{d['sdes'][0]['info']['customerId']}%22%7D%7D%5D"""
        print(df)
        r = self.session.get(df, headers=self.headers)
        print(r.content)
        data = json.loads(str(r.content).replace(d['cb'], '')[3:-3])
        self.session_id = data['sdkConf']['lpSessionId']
        self.visitor_id = data['sdkConf']['lpVisitorId']
        self.last_visit = data['sdkConf']['lpLastVisit']
        self.session.cookies.clear()
    def next_page(self, customer_id, title, url, purl):
        s = str(round(random.random() * 99999)) + "x" + str(round(random.random() * 99999))
        self.pid = abs(round(9999999999 * random.random()))
        d = {'sid': self.session_id,
             'cb': f'lpCb{s}',
             't': 'sp',
             'ts': f"{int(datetime.datetime.now().timestamp() * 1000)}",
             'pid': self.pid,
             'tid': self.tid,
             'vid': self.visitor_id,
             'rvt': self.last_visit,
             'pt': title,
             'u': url,
             'r': purl,
             'df': '0',
             'os': '1',
             'sdes': [{"type": "ctmrinfo", "info": {"customerId": f'{customer_id}'}}]}
        df = f"""https://va.v.liveperson.net/api/js/48853463?&cb={d['cb']}&t={d['t']}&ts={d['ts']}&pid={d['pid']}&tid={d['tid']}&pt=Compare%20car%20insurance%20quotes%2C%20buy%20%26%20save%20%7C%20Answer%20Financial&u=https%3A%2F%2F{d['u']}%2F&df={d['df']}&os={d['os']}&sdes=%5B%7B%22type%22%3A%22ctmrinfo%22%2C%22info%22%3A%7B%22customerId%22%3A%22{d['sdes'][0]['info']['customerId']}%22%7D%7D%5D"""

        r = self.session.get(df, headers=self.headers)
        data = json.loads(str(r.content).replace(d['cb'], '')[3:-3])
        print(data)
        self.session_id = data['sdkConf']['lpSessionId']
        self.visitor_id = data['sdkConf']['lpVisitorId']
        self.last_visit = data['sdkConf']['lpLastVisit']
        self.session.cookies.clear()

    def refresh_token(self):
        s = str(round(random.random() * 99999)) + "x" + str(round(random.random() * 99999))
        d = {'sid':self.session_id,
             'cb': f'lpCb{s}',
             't': 'ip',
             'ts': f"{int(datetime.datetime.now().timestamp() * 1000)}",
             'pid': self.pid,
             'tid': self.tid,
             'vid':self.visitor_id,
             }

        df = f"""https://va.v.liveperson.net/api/js/48853463?sid={d['sid']}&cb={d['cb']}&t={d['t']}&ts={d['ts']}&pid={d['pid']}&tid={d['tid']}&vid={d['vid']}"""
        print(df)
        r = self.session.get(df, headers=self.headers)
        data = json.loads(str(r.content).replace(d['cb'], '')[3:-3])
        print(data)
        self.session.cookies.clear()
    def page_loaded(self):
        s = str(round(random.random() * 99999)) + "x" + str(round(random.random() * 99999))
        d = {'sid': self.session_id,
             'cb': f'lpCb{s}',
             't': 'lp',
             'ts': f"{int(datetime.datetime.now().timestamp() * 1000)}",
             'pid': self.pid,
             'tid': self.tid,
             'vid': self.visitor_id
             }

        df = f"""https://va.v.liveperson.net/api/js/48853463?sid={d['sid']}&cb={d['cb']}&t={d['t']}&ts={d['ts']}&pid={d['pid']}&tid={d['tid']}&vid={d['vid']}"""
        r = self.session.get(df, headers=self.headers)
        data = json.loads(str(r.content).replace(d['cb'], '')[3:-3])
        print(data)
        self.session.cookies.clear()



