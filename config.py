import os

base_dir = os.path.dirname(os.path.abspath(__file__))

proxy_modules = [
    'crawler.ProxyDaiLi66',
    'crawler.ProxyGuoBanJia',
    'crawler.ProxyIPHai',
    'crawler.ProxyKuaiDaiLi',
    'crawler.ProxyMianFeiDaiLi',
    'crawler.ProxyWuYou',
    'crawler.ProxyXiCi',
    'crawler.ProxyYunDaiLi',

    # 'crawler.ProxyChinaIP',  # 墙外网站
]

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_KEY_RAW = 'proxy_raw'
REDIS_KEY_USEFUL = 'proxy_useful'

web_host = '0.0.0.0'
web_port = 6001

max_num = 500

interval_verify_useful = 60 * 9
interval_verify_raw = 60 * 6
interval_crawl = 60 * 12
# interval_verify_useful = 7
# interval_verify_raw = 8
# interval_crawl = 10

log_path = os.path.join(base_dir, 'logs')
