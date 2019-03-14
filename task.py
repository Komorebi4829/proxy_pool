import logging
from concurrent import futures

from common import redis
from config import REDIS_KEY_RAW, REDIS_KEY_USEFUL, max_num
from _task import _crawl_proxy, _save_to_db, _verify_proxy_raw, _verify_proxy_useful


logger = logging.getLogger('proxy_pool')


def verify_proxy_raw():
    """
    定时任务, 验证 raw 中的代理是否可用
    :return:
    """
    logger.info('开始验证 raw 代理')
    key = REDIS_KEY_RAW
    proxys = redis.hkeys(key)
    if not proxys:
        logger.info('raw 代理数量为零, 验证 done')
        return
    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        for proxy, result in zip(proxys, executor.map(_verify_proxy_raw, proxys)):
            # 无需知道结果
            pass
    logger.info('验证 raw 代理 done')


def verify_proxy_useful():
    """
    定时任务, 验证 useful 中的代理是否可用
    :return:
    """
    logger.info('开始验证 useful 代理')
    key = REDIS_KEY_USEFUL
    proxys = redis.hkeys(key)
    if not proxys:
        logger.info('useful 代理数量为零, 验证 done')
        return
    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        for proxy, result in zip(proxys, executor.map(_verify_proxy_useful, proxys)):
            # 无需知道结果
            pass
    logger.info('验证 useful 代理 done')


def crawl_proxy():
    """
    定时任务, 间隔一定时间运行一次爬虫
    :return:
    """
    logger.info('开始运行爬虫...')
    key = REDIS_KEY_USEFUL
    num = redis.hlen(key)
    if num > max_num:
        logger.info('代理数量大于{}, 停止爬取'.format(max_num))
        return

    for ip_ports in _crawl_proxy():
        _save_to_db(ip_ports)
    logger.info('爬取任务 done')


def main():
    pass


if __name__ == '__main__':
    main()
