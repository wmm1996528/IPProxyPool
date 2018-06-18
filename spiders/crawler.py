import requests
from db import redisIP
from lxml import etree
from test import iptest
from pyquery import PyQuery as pq
from multiprocessing import Process
from threading import Thread
import re
import time
from setting import looger


class CrawlerMettaClass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(v)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=CrawlerMettaClass):
    def __init__(self):
        self.ip_lists = set()

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }
    def get_html(self, url):

        res = requests.get(url, headers=self.headers, verify=False, timeout=2)
        return res.text

    def crawl_xici(self, ):
        looger.warning('抓取xici')
        url = 'http://www.xicidaili.com/nn/{}'
        for i in range(1, 3):
            res = self.get_html(url.format(i))
            html = etree.HTML(res)
            datas = html.xpath('//table[@id="ip_list"]/tr')

            for data in datas:
                try:
                    host = data.xpath('td[2]/text()')[0]
                    port = data.xpath('td[3]/text()')[0]
                    state = data.xpath('td[6]/text()')[0]

                    self.ip_lists.add(host + ':' + port)

                except Exception as e:
                    pass

    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        looger.warning('抓取daili66')
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            html = self.get_html(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    self.ip_lists.add(':'.join([ip, port]))

    def crawl_89ip(self):
        looger.warning('抓取89ip')
        url = 'http://www.89ip.cn/tqdl.html?api=1&num=100&port=&address=&isp='
        html = self.get_html(url)
        if html:
            find_ips = re.compile('(\d+\.\d+\.\d+\.\d+:\d+)', re.S)
            ip_ports = find_ips.findall(html)
            iptest.start(ip_ports)

    def crawl_ip3366(self):
        try:
            looger.warning('抓取ip3366')
            for i in range(1, 4):
                start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
                html = self.get_html(start_url)
                if html:
                    find_tr = re.compile('<tr>(.*?)</tr>', re.S)
                    trs = find_tr.findall(html)
                    for s in range(1, len(trs)):
                        find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                        re_ip_address = find_ip.findall(trs[s])
                        find_port = re.compile('<td>(\d+)</td>')
                        re_port = find_port.findall(trs[s])
                        for address, port in zip(re_ip_address, re_port):
                            address_port = address + ':' + port
                            self.ip_lists.add(address_port)
        except:
            pass

    def crawl_kuaidaili(self):
        headers = {
            'Referer': 'Referer: https://www.kuaidaili.com/free/inha/'
        }
        looger.warning('抓取快代理')
        for i in range(1, 4):

            url = 'https://www.kuaidaili.com/free/inha/{}'.format(i)

            html = requests.get(url, headers=headers).text
            doc = etree.HTML(html)
            trs = doc.xpath('//*[@id="list"]/table/tbody/tr')
            for i in trs:
                self.ip_lists.add(i.xpath('td[1]/text()')[0] + ':' + i.xpath('td[2]/text()')[0])

    def crawl_yundaili(self):
        headers = {
            'Referer': 'Referer: https://www.kuaidaili.com/free/inha/'
        }
        looger.warning('抓取云代理')
        for i in range(1, 6):
            url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
            print(url)
            html = requests.get(url, headers=self.headers, timeout=2, verify=False).text
            doc = etree.HTML(html)
            trs = doc.xpath('//*[@id="list"]/table/tbody/tr')
            for tr in trs:
                self.ip_lists.add(tr.xpath('td[1]/text()')[0] + ':' + tr.xpath('td[2]/text()')[0])

    def run(self):
        looger.warning('刷新ip')
        threads = []
        # self.crawl_yundaili()
        print(len(self.ip_lists))
        self.crawl_89ip()
        self.crawl_daili66()
        self.crawl_ip3366()
        self.crawl_kuaidaili()
        self.crawl_xici()
        print(len(self.ip_lists))
        iptest.start(self.ip_lists)
        # for i in range(len(threads)):
        #     try:
        #         threads[i].start()
        #     except Exception as e:
        #         print(e)
        # for i in range(len(threads)):
        #     threads[i].join()
        looger.warning('刷新成功， 目前数量为：%s' % redisIP.get_ip_size())


CrawlSpiders = Crawler()

if __name__ == '__main__':
    CrawlSpiders.crawl_yundaili()
