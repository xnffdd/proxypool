#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
全局配置
'''

'''
日志配置
'''
LOG_LEVEL = 'INFO'  # 日志级别 ['DEBUG','WARNING','INFO','ERROR']
LOG_FILE_USE = True  # 日志是否存储到文件
LOG_FILE = 'app'  # 日志存储文件名
LOG_STREAM_USE = True  # 日志是否打印到控制台

'''
MySQL数据库连接配置
'''
DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, TABLE_NAME = (
    '127.0.0.1', 3306, 'test', 'root', 'root', 'proxy')  # MySQL配置

'''
IP免费代理抓取爬虫配置
'''
GRAB_INTERVAL_MINUTES = 15  # 周期抓取任务间隔（分钟）（注意比下面的大）
ALL_GRAB_GEVENT_TIMEOUT = 8 * 60  # 所有爬取协程任务总限时（秒）
SPIDER_MAX_ATTEMPT_NUMBER = 10  # 单个网站爬虫插件失败重试次数

'''
在线验证IP代理有效性服务配置
'''
VERIFY_INTERVAL_MINUTES = 10  # 周期验证任务间隔（分钟）（注意比下面的大）
ALL_VERIFY_GEVENT_TIMEOUT = 5 * 60  # 所有验证协程任务总限时（秒）
CHECK_PROXY_HOUR_THRESHOL = 7 * 24  # 抓取时间在{VALID_PROXY_HOUR_THRESHOLD}（小时）内 或 验证时间在{VALID_PROXY_HOUR_THRESHOLD}（小时）内的代理为待持续验证的代理

'''
Web服务配置
'''
VALID_PROXY_HOUR_THRESHOLD = 1 * 24  # 验证时间在{VALID_PROXY_HOUR_THRESHOLD}（小时）内的代理鉴定为可用代理
WEB_SERVER_HOST, WEB_SERVER_PORT = 'localhost', 9999  # Local Web Service 提供可用代理服务
