from apscheduler.schedulers.background import BackgroundScheduler

from task import verify_proxy_raw, verify_proxy_useful, crawl_proxy
import config


def start_crawl_scheduler():
    scheduler = BackgroundScheduler()
    seconds = config.interval_crawl
    scheduler.add_job(crawl_proxy, "interval", seconds=seconds, id="crawl")
    scheduler.start()


def start_verify_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(verify_proxy_useful, 'interval', seconds=config.interval_verify_useful, id="verify_proxy_useful")
    scheduler.add_job(verify_proxy_raw, 'interval', seconds=config.interval_verify_raw, id="verify_proxy_raw")
    scheduler.start()
