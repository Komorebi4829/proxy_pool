import logging

from common import redis
from util import check
from util import import_string
from config import REDIS_KEY_RAW, REDIS_KEY_USEFUL, proxy_modules


logger = logging.getLogger('proxy_pool')


def _verify_proxy_raw(proxy):
    """
    如果可用: 放入 useful
       不可用: 丢弃
    :param proxy:
    :return:
    """
    if not redis.hexists(REDIS_KEY_RAW, proxy):
        return

    available = check(proxy)
    if available is True:
        redis.hdel(REDIS_KEY_RAW, proxy)
        redis.hset(REDIS_KEY_USEFUL, proxy, '1')
    else:
        redis.hdel(REDIS_KEY_RAW, proxy)


def _verify_proxy_useful(proxy):
    """
    如果可用: 保留
       不可用: 放入 raw
    :param proxy:
    :return:
    """
    if not redis.hexists(REDIS_KEY_USEFUL, proxy):
        return

    available = check(proxy)
    if available is True:
        pass
    else:
        redis.hdel(REDIS_KEY_USEFUL, proxy)
        redis.hset(REDIS_KEY_RAW, proxy, '1')


def _crawl_proxy():
    for module in proxy_modules:
        Proxy = import_string(module)
        p = Proxy()
        logger.info('running: {}.crawl'.format(p.__class__.__name__))
        ip_ports = p.crawl()
        yield ip_ports


def _save_to_db(ip_ports):
    for proxy in ip_ports:
        if proxy and check(proxy):
            redis.hset(REDIS_KEY_USEFUL, proxy, '1')
