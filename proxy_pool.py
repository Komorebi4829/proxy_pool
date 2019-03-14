import os
import time
import random
import logging

import config
from common import redis


class ProxyPool(object):
    def __init__(self):
        self.max_num = config.max_num
        self.interval_verify_useful = config.interval_verify_useful
        self.interval_verify_raw = config.interval_verify_raw
        self.interval_crawl = config.interval_crawl
        self.log = None
        self.init_logging()

    def init_logging(self):
        log_path = config.log_path
        if not os.path.exists(log_path):
            os.mkdir(log_path)

        today = time.strftime('%Y-%m-%d', time.localtime())
        name = "proxy_pool_" + today
        filename = os.path.join(log_path, name)
        log = logging.getLogger("proxy_pool")
        f = '%(asctime)s [%(name)s] %(filename)s(+%(lineno)d) %(levelname)s: %(message)s'
        fm = logging.Formatter(f)
        log.setLevel(logging.DEBUG)
        if filename:
            handler = logging.FileHandler(filename, encoding="utf-8")
            handler.setFormatter(fm)
            log.addHandler(handler)

        console = logging.StreamHandler()
        console.setFormatter(fm)
        console.setLevel(logging.INFO)
        log.addHandler(console)
        self.log = log

    @staticmethod
    def get():
        proxys = redis.hkeys(config.REDIS_KEY_USEFUL)
        if not proxys:
            return 'empty proxy'
        return random.choice(proxys)

    @staticmethod
    def count():
        n = redis.hlen(config.REDIS_KEY_USEFUL)
        return n
