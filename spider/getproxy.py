#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import json
import time
import logging

import requests
import gevent.pool
import gevent.monkey
import geoip2.database

from config import ALL_GRAB_GEVENT_TIMEOUT, ALL_VERIFY_GEVENT_TIMEOUT, VALID_PROXY_HOUR_THRESHOLD
from util.utils import load_object, get_current_time_str
from util.http import user_agent
from db.manager import ProxyDBManager

gevent.monkey.patch_all()

logger = logging.getLogger(__name__)
base_dir = os.path.dirname(os.path.realpath(__file__))

PROXY_PROTOCOL_HTTP = 'http'
PROXY_PROTOCOL_HTTPS = 'https'

PROXY_ANONYMITY_TRANSPARENT = 'transparent'
PROXY_ANONYMITY_ANONYMOUS = 'anonymous'
PROXY_ANONYMITY_HIGH_ANONYMOUS = 'high_anonymous'


class Plugin(object):
    def __init__(self):
        self.name = None
        self.result = []
        self.proxies = []
        self.cur_proxy = None
        self.protocol = None
        self.anonymity = None
        self.session = requests.session()

    def start(self):
        raise NotImplemented

    def _change_self_proxy(self):
        while self.proxies:
            new_proxy = self.proxies.pop(0)

            _protocol = new_proxy.get('protocol')
            _anonymity = new_proxy.get('anonymity')
            _host = new_proxy.get('host')
            _port = new_proxy.get('port')

            if self.protocol and self.protocol != _protocol:
                continue
            if self.anonymity and self.anonymity != _anonymity:
                continue

            self.cur_proxy = {_protocol: "%s:%s" % (_host, _port)}
            logger.info(
                'switched spider plugin(%s) self proxy to Proxy(protocol: %s, host: %s, port: %s)' % (
                    self.name, _protocol, _host, _port))

    def _log(self, _logger, msg, url, error):
        _logger.error(
            '{msg}, spider plugin: {plugin}, url: {url}, error: {error}'.format(msg=msg, plugin=self.name, url=url,
                                                                                error=error))

    def _need_retry(self):
        self.change_self_proxy()
        raise Exception('retry spider plugin({plugin})...'.format(plugin=self.name))


class GrabProxy(object):
    def __init__(self):
        self.pool = gevent.pool.Pool(500)
        self.plugins = []
        self.web_proxies = []
        _manager = ProxyDBManager()
        self.proxies = _manager.get_all_valid_proxy(VALID_PROXY_HOUR_THRESHOLD)
        _manager.close()

    def _collect_result(self):
        for plugin in self.plugins:
            logger.info('spider plugin(%s) grabbed %s proxies' % (plugin.name, len(plugin.result)))
            if plugin.result:
                self.web_proxies.extend(plugin.result)

    def load_plugins(self):
        logger.info("load spider plugins...")

        for plugin_name in os.listdir(os.path.join(base_dir, 'plugin')):
            if os.path.splitext(plugin_name)[1] != '.py' or plugin_name == '__init__.py':
                continue
            try:
                cls = load_object("spider.plugin.%s.Proxy" % os.path.splitext(plugin_name)[0])
            except Exception as e:
                logger.error("load spider plugin %s failed, error: %s" % (plugin_name, str(e)))
                continue
            inst = cls()
            inst.proxies = self.proxies
            logger.info('loaded spider plugin({name}), attach {count} proxies to it'.format(name=inst.name,
                                                                                            count=len(inst.proxies)))
            self.plugins.append(inst)

        logger.info("loaded %s spider plugins" % len(self.plugins))

    def grab_web_proxies(self):
        logger.info("grab proxies...")

        for plugin in self.plugins:
            self.pool.spawn(plugin.start)
        self.pool.join(timeout=ALL_GRAB_GEVENT_TIMEOUT)
        self.pool.kill()
        self._collect_result()

        logger.info("grabbed %s proxies" % len(self.web_proxies))

    def start(self):
        self.load_plugins()
        self.grab_web_proxies()


class VerifyProxy(object):
    def __init__(self):
        self._pool = gevent.pool.Pool(500)
        self._origin_ip = None
        self._geoip_reader = None

        self._init()

    def _init(self):
        logger.info("init proxy verify system...")

        rp = requests.get(url='http://httpbin.org/get', headers={'user-agent': user_agent()})
        self._origin_ip = rp.json().get('origin', '')
        logger.info("current local ip address: %s" % self._origin_ip)

        self._geoip_reader = geoip2.database.Reader(os.path.join(base_dir, 'data/GeoLite2-Country.mmdb'))

    def validate_web_proxies(self, web_proxies):
        logger.info("validate proxies...")

        valid_proxies = self._validate_proxy_list(web_proxies)
        logger.info("checked %s proxies, got %s valid proxies" % (len(web_proxies), len(valid_proxies)))

        return valid_proxies

    def _validate_proxy_list(self, proxies):
        valid_proxies = []

        def save_result(p):
            if p:
                valid_proxies.append(p)

        for proxy in proxies:
            self._pool.apply_async(self._validate_proxy, args=(proxy, PROXY_PROTOCOL_HTTP), callback=save_result)
            self._pool.apply_async(self._validate_proxy, args=(proxy, PROXY_PROTOCOL_HTTPS), callback=save_result)

        self._pool.join(timeout=ALL_VERIFY_GEVENT_TIMEOUT)
        self._pool.kill()

        return valid_proxies

    def _validate_proxy(self, proxy, protocol):
        host = proxy.get('host')
        port = proxy.get('port')
        request_proxies = {protocol: "%s:%s" % (host, port)}

        request_begin = time.time()

        try:
            response_json = requests.get(
                "%s://httpbin.org/get?show_env=1&cur=%s" % (protocol, request_begin),
                proxies=request_proxies,
                timeout=5
            ).json()
        except:
            return

        request_end = time.time()

        if not isinstance(response_json, dict) or str(request_begin) != response_json.get('args', {}).get('cur', ''):
            return

        anonymity = self._check_proxy_anonymity(response_json)
        country = proxy.get('country')
        country = country or self._geoip_reader.country(host).country.iso_code
        export_address = self._check_export_address(response_json)

        return {
            "protocol": protocol,
            "host": host,
            "export_address": export_address,
            "port": port,
            "anonymity": anonymity,
            "country": country,
            "response_time": round(request_end - request_begin, 2),
            "from": proxy.get('from'),
            'grab_time': proxy.get('grab_time'),
            'check_time': get_current_time_str()
        }

    def _check_proxy_anonymity(self, response):
        via = response.get('headers', {}).get('Via', '')

        if self._origin_ip in json.dumps(response):
            return PROXY_ANONYMITY_TRANSPARENT
        elif via and via != "1.1 vegur":
            return PROXY_ANONYMITY_ANONYMOUS
        else:
            return PROXY_ANONYMITY_HIGH_ANONYMOUS

    def _check_export_address(self, response):
        origin = response.get('origin', '').split(', ')

        if self._origin_ip in origin:
            origin.remove(self._origin_ip)

        return origin


def duplicate_filter(proxies):
    proxies_dict = {}

    for proxy in proxies:
        proxy_hash = '%s:%s' % (proxy.get('host'), proxy.get('port'))
        proxies_dict[proxy_hash] = proxy

    return list(proxies_dict.values())


def save(proxies, output_proxies_file=None):
    if output_proxies_file:
        outfile = open(output_proxies_file, 'w')
    else:
        outfile = sys.stdout

    for item in proxies:
        outfile.write("%s\n" % json.dumps(item))

    outfile.flush()
    if outfile != sys.stdout:
        outfile.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    grab = GrabProxy()
    grab.start()
    proxies = grab.web_proxies

    unique_proxies = duplicate_filter(proxies)

    verfy = VerifyProxy()
    valid_proxies = verfy.validate_web_proxies(unique_proxies)

    save(valid_proxies, output_proxies_file='proxy.txt')
