from flask import Flask, make_response
from db import *
from test import iptest
from spiders.crawler import CrawlSpiders


app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Welcome To IP ProxyPool !</h1>'

@app.route('/ip')
def get_ip():
    while True:
        if redisIP.get_ip_size() == 0:
            return None
        proxy = redisIP.get_ip()
        return proxy

@app.route('/all')
def get_all():
    return redisIP.get_ips()

@app.route('/cookie')
def get_cookie():
    return cookiepool.get_ip()

@app.route('/size')
def get_size():
    return make_response('ip可用数量为：%s' % redisIP.get_ip_size())




if __name__ == '__main__':
    app.run()