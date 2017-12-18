#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import logging

from flask import Flask, jsonify, request

from db.manager import ProxyDBManager
from config import WEB_SERVER_HOST, WEB_SERVER_PORT, VALID_PROXY_HOUR_THRESHOLD
from spider.getproxy import PROXY_PROTOCOL_HTTP, PROXY_PROTOCOL_HTTPS
from spider.getproxy import PROXY_ANONYMITY_TRANSPARENT, PROXY_ANONYMITY_ANONYMOUS, PROXY_ANONYMITY_HIGH_ANONYMOUS
from web.constant import api_help

logger = logging.getLogger(__file__)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def index():
    return jsonify(api_help)


@app.route('/get/')
def get():
    try:
        _kw = get_request_kws()
    except:
        return jsonify({
            'ret': 1080,
            'msg': 'invalid argument'
        })
    try:
        _proxy = get_one(**_kw)
        if _proxy:
            return jsonify({
                'ret': 0,
                'data': _proxy
            })
        else:
            return jsonify({
                'ret': 1090,
                'msg': 'empty'
            })
    except Exception as e:
        logger.error("web server internal error, error: %s" % str(e))
        return jsonify({
            'ret': -1001,
            'msg': 'web server internal error'
        })


@app.route('/get_all/')
def get_all():
    try:
        _kw = get_request_kws()
    except:
        return jsonify({
            'ret': 1080,
            'msg': 'invalid argument'
        })
    try:
        _proxies = get(**_kw)
        if _proxies:
            return jsonify({
                'ret': 0,
                'data': _proxies
            })
        else:
            return jsonify({
                'ret': 1090,
                'msg': 'empty'
            })
    except Exception as e:
        logger.error("web server internal error, error: %s" % str(e))
        return jsonify({
            'ret': -1002,
            'msg': 'web server internal error'
        })


def get_request_kws():
    check_in_hour = request.args.get('check_in_hour')
    if check_in_hour is not None:
        check_in_hour = float(check_in_hour)
        if check_in_hour <= 0:
            raise ValueError
    else:
        check_in_hour = VALID_PROXY_HOUR_THRESHOLD

    protocol = request.args.get('protocol')
    if protocol is not None:
        if protocol not in (PROXY_PROTOCOL_HTTP, PROXY_PROTOCOL_HTTPS):
            raise ValueError

    anonymity = request.args.get('anonymity')
    if anonymity is not None:
        if anonymity not in (PROXY_ANONYMITY_TRANSPARENT, PROXY_ANONYMITY_ANONYMOUS, PROXY_ANONYMITY_HIGH_ANONYMOUS):
            raise ValueError

    response_time_in_second = request.args.get('response_time_in_second')
    if response_time_in_second is not None:
        response_time_in_second = float(response_time_in_second)
        if response_time_in_second <= 0:
            raise ValueError

    return {
        'check_in_hour': check_in_hour,
        'protocol': protocol,
        'anonymity': anonymity,
        'response_time_in_second': response_time_in_second,
    }


def get_one(check_in_hour, protocol, anonymity, response_time_in_second):
    lst = get(check_in_hour, protocol, anonymity, response_time_in_second)
    return random.choice(lst) if lst else {}


def get(check_in_hour, protocol, anonymity, response_time_in_second):
    manager = ProxyDBManager()
    proxies = manager.get_all_valid_proxy(check_in_hour)
    manager.close()

    def _filter(proxy):
        if protocol is not None and proxy.get('protocol') != protocol:
            return False
        if anonymity is not None and proxy.get('anonymity') != anonymity:
            return False
        if response_time_in_second is not None and (proxy.get('response_time') or 0) > response_time_in_second:
            return False
        return True

    return list(filter(_filter, proxies))


def start_web_server():
    logger.info('start web server...')
    app.run(host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == '__main__':
    proxies = get(protocol='http', anonymity='high_anonymous', response_time=1.0)
    print(proxies)

    print(get_one())

    start_web_server()
