from apscheduler.schedulers.blocking import BlockingScheduler

from task import verify_proxy_raw, verify_proxy_useful, crawl_proxy
import config


def crawl():
    scheduler = BlockingScheduler()
    seconds = config.interval_crawl
    scheduler.add_job(crawl_proxy, "interval", seconds=seconds, id="crawl")
    scheduler.start()


def verify_useful():
    scheduler = BlockingScheduler()
    seconds = config.interval_verify_useful
    scheduler.add_job(verify_proxy_useful, 'interval', seconds=seconds, id="verify_proxy_useful")
    scheduler.start()


def verify_raw():
    scheduler = BlockingScheduler()
    seconds = config.interval_verify_raw
    scheduler.add_job(verify_proxy_raw, 'interval', seconds=seconds, id="verify_proxy_raw")
    scheduler.start()
