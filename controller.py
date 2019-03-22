from concurrent import futures

import scheduler
from proxy_pool import ProxyPool
from task import crawl_proxy, verify_proxy_raw
from app import run as run_app


proxy_pool = ProxyPool()


def start_service():
    funcs = [
        scheduler.start_crawl_scheduler,
        scheduler.start_verify_scheduler,
        run_app,
    ]
    tasks = []
    with futures.ProcessPoolExecutor(max_workers=3) as executor:
        crawl = executor.submit(funcs[0])
        verify = executor.submit(funcs[1])
        app = executor.submit(funcs[2])
        tasks.append([crawl, verify, app])

    crawl_proxy()
    verify_proxy_raw()


def serve_forever():
    print('start service...')
    start_service()
