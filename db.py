import redis

class  Data():
    def __init__(self, key):
        self.db = redis.from_url('redis://127.0.0.1:6379')
        self.key = key
    def put(self, item):
        if isinstance(item, list):
            for i in item:
                self.db.sadd(self.key, i)
        else:
            self.db.sadd(self.key, item)


    def get_ip_size(self):
        '''
        获取可用ip数量
        :return:
        '''
        return self.db.scard(self.key)

    def get_ip(self):
        '''
        获取一个ip
        :return: 一个ip
        '''
        return self.db.spop(self.key)


    def get_ips(self):
        '''
        获取所有IP
        :return: list(ip)
        '''
        return self.db.smembers(self.key)

redisIP = Data('ips')
cookiepool = Data('cookies')