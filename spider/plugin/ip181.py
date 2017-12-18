#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import logging

import retrying

from config import SPIDER_MAX_ATTEMPT_NUMBER
from util.http import headers
from util.utils import get_current_time_str
from spider.getproxy import Plugin, PROXY_PROTOCOL_HTTP, PROXY_ANONYMITY_HIGH_ANONYMOUS

logger = logging.getLogger(__name__)


class Proxy(Plugin):
    def __init__(self):
        Plugin.__init__(self)

        self.name = 'IP181'
        self.protocol = PROXY_PROTOCOL_HTTP
        self.anonymity = PROXY_ANONYMITY_HIGH_ANONYMOUS

        self.host = 'www.ip181.com'
        self.url_template = 'http://www.ip181.com/'
        self.re_ip_port_pattern = re.compile(
            r"<tr>\s+<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>\s+<td>(\d{1,5})</td>", re.I)

    @retrying.retry(stop_max_attempt_number=SPIDER_MAX_ATTEMPT_NUMBER)
    def _extract_proxy(self):
        try:
            full_url = self.url_template
            rp = self.session.get(url=full_url, headers=headers(host=self.host), timeout=10)
        except Exception as e:
            self._log(logger, 'request error', full_url, str(e))
            self._need_retry()

        re_ip_port_result = self.re_ip_port_pattern.findall(rp.text)

        if not re_ip_port_result:
            self._log(logger, 'extract data error', full_url, 'find no proxy data in web page')
            self._need_retry()

        return [{'host': host, 'port': port, 'from': self.name, 'grab_time': get_current_time_str()}
                for host, port in re_ip_port_result]

    def start(self):
        try:
            page_result = self._extract_proxy()
            if page_result:
                self.result.extend(page_result)
        except Exception as e:
            logger.error(str(e))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    p = Proxy()
    p.start()
    for i in p.result:
        print(i)
