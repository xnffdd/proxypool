#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from schedule.task import start_background_scheduler
from db.manager import check_database
from web.manager import start_web_server
from util.log import log_init


def main():
    log_init()
    check_database()
    start_background_scheduler()
    start_web_server()


if __name__ == '__main__':
    main()
