#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from apscheduler.schedulers.background import BackgroundScheduler

from db.manager import ProxyDBManager
from spider.getproxy import GrabProxy, VerifyProxy, duplicate_filter
from config import GRAB_INTERVAL_MINUTES, VERIFY_INTERVAL_MINUTES,CHECK_PROXY_HOUR_THRESHOL

logger = logging.getLogger(__file__)


def grab_task():
    try:
        logger.info('run grab job...')

        grab = GrabProxy()
        grab.start()
        proxies = grab.web_proxies

        unique_proxies = duplicate_filter(proxies)

        verfy = VerifyProxy()
        valid_proxies = verfy.validate_web_proxies(unique_proxies)

        dbManager = ProxyDBManager()
        dbManager.replace_insert(valid_proxies)
        dbManager.close()

        logger.info('grab job finished')
    except Exception as e:
        logger.error('grab job failed, error: %s' % str(e))


def verify_task():
    try:
        logger.info('run verify job...')

        dbManager = ProxyDBManager()
        proxies = dbManager.get_all_proxy_for_check(CHECK_PROXY_HOUR_THRESHOL)

        verfy = VerifyProxy()
        valid_proxies = verfy.validate_web_proxies(proxies)

        dbManager.replace_insert(valid_proxies)
        dbManager.close()

        logger.info('grab verify finished')
    except Exception as e:
        logger.error('verify job failed, error: %s' % str(e))


def start_background_scheduler():
    logger.info('start background scheduler...')

    sched = BackgroundScheduler()
    sched.add_job(grab_task, 'interval', minutes=GRAB_INTERVAL_MINUTES)
    sched.add_job(verify_task, 'interval', minutes=VERIFY_INTERVAL_MINUTES)
    sched.start()

    logger.info('background scheduler started')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    start_background_scheduler()
