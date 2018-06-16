import time
from multiprocessing import Process
from threading import Thread
from setting import *
from logging import getLogger
from api import app
from db import *
from cookies import cookies
from spiders.crawler import CrawlSpiders

logger = getLogger('ip')
class Scheduler():
    def scheduler_crawler(self):
        while True:
            if redisIP.get_ip_size() < 10:
                CrawlSpiders.run()


    def scheduler_api(self):
        app.run(API_HOST, API_PORT)

    def scheduler_cookies(self):
        while True:
            if cookiepool.get_ip_size() < 1:
                cookies.run()
    def run(self):
        looger.warning('IP代理池开始运行')
        looger.warning('当前可用数量为：%s' % redisIP.get_ip_size())
        logger.warning('''\n\t/ip 获取一个可用IP\n\t/all 获取所有IP\n\t/size 获取可用IP数量\n''')
        crawler_process = Process(target=self.scheduler_crawler)
        crawler_process.start()
        crawler_cookies = Process(target=self.scheduler_cookies)
        crawler_cookies.start()
        api_process = Process(target=self.scheduler_api)
        api_process.start()


if __name__ == '__main__':
    s = Scheduler()
    s.run()


