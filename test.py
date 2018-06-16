import requests
import gevent
from db import redisIP
import urllib3
urllib3.disable_warnings()
class IPTest():
    def __init__(self,testUtl):
        self.url = testUtl

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }

    def start(self, ips):
        jobs = [gevent.spawn(self.test, ip) for ip in ips]
        gevent.joinall(jobs, timeout=2)
    def test(self, ip):
        proxy = {
            'http': 'http://'+str(ip),
            'https': 'https://'+str(ip),
        }
        try:
            res = requests.get(self.url, headers=self.headers, proxies=proxy, timeout=2, verify=False)
            if res.status_code == 200:
                # print('{}:可用'.format(ip))
                redisIP.put(ip)
        except Exception as e:
            pass
    def test_one(self, ip):
        if ip == None:
            return
        proxy = {
                'http': 'http://'+str(ip),
                'https': 'https://'+str(ip),
        }
        try:
            res = requests.get(self.url, headers=self.headers, proxies=proxy, timeout=2, verify=False)
            if res.status_code == 200:
                print('{}:可用'.format(ip))
                return True
        except Exception as e:
            return  None




iptest = IPTest('https://www.baidu.com')


# if __name__ == '__main__':
#     s=  [{'host': '183.149.47.96', 'port': '51210', 'addr': '江苏常州', 'state': 'HTTPS', 'speed': '0.133秒', 'delay': '0.026秒'}]
#     iptest.start(s)