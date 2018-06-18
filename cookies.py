from db import *
from weibo import Launcher
from setting import *


class CookiePool():

    def get_new(self, user, pwd):
        l = Launcher(user, pwd)
        cookie = l.login()
        cookiepool.put(cookie)

    def run(self):
        for i in USERINFO:
            self.get_new(i['username'], i['password'])


cookies = CookiePool()
if __name__ == '__main__':
    s = CookiePool()
    s.run()
