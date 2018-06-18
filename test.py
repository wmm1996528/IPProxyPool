import requests
import gevent
from db import redisIP
import aiohttp
import asyncio
import urllib3
import json
import re
import traceback

urllib3.disable_warnings()


class IPTest():
    def __init__(self, testUtl):
        self.url = testUtl

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }

    def start(self, ips):
        if len(ips) == 0:
            return
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [self.test(ip) for ip in ips]
        loop.run_until_complete(asyncio.wait(tasks))

    async def test(self, ip):
        async with aiohttp.ClientSession() as session:

            try:
                async with session.get(self.url, headers=self.headers, proxy='http://' + ip, timeout=2,
                                       verify_ssl=False) as res:

                    if res.status == 200:
                        data = json.loads(await res.text())
                        # print(data['headers']['X-Forwarded-For'])
                        # print(data)
                        if data['headers']['X-Forwarded-For'] == re.findall('\d+\.\d+\.\d+\.\d+', ip)[0]:
                            print('{}:可用'.format(ip))
                            redisIP.put(ip)

            except Exception as e:
                # print(traceback.format_exc())
                pass

    def test_one(self, ip):
        if ip == None:
            return
        proxy = {
            'http': 'http://' + str(ip),
            'https': 'https://' + str(ip),
        }
        try:
            res = requests.get(self.url, headers=self.headers, proxies=proxy, timeout=2, verify=False)
            if res.status_code == 200:
                print('{}:可用'.format(ip))
                return True
        except Exception as e:
            return None


iptest = IPTest('http://httpbin.org/get?show_env=1')

if __name__ == '__main__':
    s = [{'host': '183.149.47.96', 'port': '51210', 'addr': '江苏常州', 'state': 'HTTPS', 'speed': '0.133秒',
          'delay': '0.026秒'}]
    iptest.start(s)
