#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config import VALID_PROXY_HOUR_THRESHOLD
from spider.getproxy import PROXY_PROTOCOL_HTTP, PROXY_PROTOCOL_HTTPS
from spider.getproxy import PROXY_ANONYMITY_TRANSPARENT, PROXY_ANONYMITY_ANONYMOUS, PROXY_ANONYMITY_HIGH_ANONYMOUS

_arguments = [
    {
        'name': 'check_in_hour',
        'required': False,
        'type': 'float',
        'default': VALID_PROXY_HOUR_THRESHOLD,
        'description': 'the check time(hours) within now'
    },
    {
        'name': 'protocol',
        'required': False,
        'type': 'string',
        'default': None,
        'description': 'proxy protocol, %s' % ((PROXY_PROTOCOL_HTTP, PROXY_PROTOCOL_HTTPS),)
    },
    {
        'name': 'anonymity',
        'required': False,
        'type': 'string',
        'default': None,
        'description': 'proxy anonymity, %s' % (
            (PROXY_ANONYMITY_TRANSPARENT, PROXY_ANONYMITY_ANONYMOUS, PROXY_ANONYMITY_HIGH_ANONYMOUS),)
    }, {
        'name': 'response_time_in_second',
        'required': False,
        'type': 'float',
        'default': None,
        'description': 'the response time(seconds) within'
    }
]

api_help = {
    'http api': [
        {
            'description': 'get an usable proxy',
            'url': '/get',
            'method': 'GET',
            'arguments': _arguments,
            'return': {
                'ret': 'the return code, 0 means success',
                'msg': 'error message',
                'data': 'the return data'
            }
        },
        {
            'description': 'get all usable proxies',
            'url': '/get_all',
            'method': 'GET',
            'arguments': _arguments,
            'return': {
                'ret': 'the return code, 0 means success',
                'msg': 'error message',
                'data': 'the return data'
            }
        }
    ]
}
