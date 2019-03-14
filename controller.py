from concurrent import futures

import scheduler
from proxy_pool import ProxyPool
from task import crawl_proxy, verify_proxy_raw
from app import run as run_app


proxy_pool = ProxyPool()


def start_service():
    funcs = [
        scheduler.crawl,
        scheduler.verify_raw,
        scheduler.verify_useful,
        run_app,
    ]
    tasks = []
    for func in funcs:
        executor = futures.ProcessPoolExecutor(max_workers=1)
        future = executor.submit(func)
        tasks.append(future)

    crawl_proxy()
    verify_proxy_raw()


def serve_forever():
    print('start service...')
    start_service()
