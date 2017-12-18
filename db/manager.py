#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import datetime

import pymysql

from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, TABLE_NAME
from config import VALID_PROXY_HOUR_THRESHOLD, CHECK_PROXY_HOUR_THRESHOL
from util.utils import datetime2str

logger = logging.getLogger(__file__)


def connect():
    try:
        con = pymysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, port=DB_PORT, charset='utf8')
        logger.debug('connected MySQL')
        return con
    except Exception as e:
        logger.error(e)
        raise Exception('connect MySQL failed')


def check_database():
    logger.info('check MySQL...')
    try:
        db_manager = ProxyDBManager()
        db_manager.replace_insert([])
        db_manager.close()
    except Exception as e:
        logger.error('error happened when check MySQL database and table, error: %s' % str(e))
        raise Exception('MySQL initialization failed')


class ProxyDBManager(object):
    def __init__(self):
        self._conn = connect()
        self._cursor = self._conn.cursor()

    def replace_insert(self, proxies):
        lst = [(proxy.get('protocol'), proxy.get('host'), proxy.get('port'), proxy.get('anonymity'),
                proxy.get('country'), ' '.join(proxy.get('export_address') or []), proxy.get('response_time'),
                proxy.get('from'), proxy.get('grab_time'), proxy.get('check_time')) for proxy in proxies]

        sql = "replace into {table_name}(protocol,host,port,anonymity,country,export_address,response_time," \
              "`from`,grab_time,check_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);".format(table_name=TABLE_NAME)

        try:
            self._cursor.executemany(sql, lst)
            self._conn.commit()
            logger.info('replace insert %s proxies into MySQL' % len(lst))
        except Exception as e:
            logger.error(e)
            raise Exception('execute insert sql error')

    def get_all_proxy_for_check(self, grab_or_check_in_hour):
        now = datetime.datetime.now()
        grab_or_check_time = datetime2str(now - datetime.timedelta(hours=grab_or_check_in_hour))

        sql = "select protocol,host,port,anonymity,country,export_address,response_time,`from`,grab_time,check_time" \
              " from {table_name} where grab_time>='{grab_or_check_time}' or check_time>='{grab_or_check_time}' order by" \
              " check_time desc ,grab_time desc;".format(table_name=TABLE_NAME, grab_or_check_time=grab_or_check_time)

        try:
            self._cursor.execute(sql)
            tup = self._cursor.fetchall()
            logger.info('fetched %s proxies from MySQL' % len(tup))
        except Exception as e:
            logger.error(e)
            raise Exception('execute query sql error')

        return self._tuples2dicts(tup)

    def get_all_valid_proxy(self, check_in_hour):
        now = datetime.datetime.now()
        check_time = datetime2str(now - datetime.timedelta(hours=check_in_hour))

        sql = "select protocol,host,port,anonymity,country,export_address,response_time,`from`,grab_time,check_time" \
              " from {table_name} where check_time>='{check_time}' order by" \
              " check_time desc ,grab_time desc;".format(table_name=TABLE_NAME, check_time=check_time)

        try:
            self._cursor.execute(sql)
            tup = self._cursor.fetchall()
            logger.info('fetched %s proxies from MySQL' % len(tup))
        except Exception as e:
            logger.error(e)
            raise Exception('execute query sql error')

        return self._tuples2dicts(tup)

    def _tuples2dicts(self, tuples):
        proxies = []

        for element in tuples:
            proxies.append({
                'protocol': element[0],
                'host': element[1],
                'port': element[2],
                'anonymity': element[3],
                'country': element[4],
                'export_address': (element[5] or '').split(),
                'response_time': element[6],
                'from': element[7],
                'grab_time': datetime2str(element[8]) if element[8] else None,
                'check_time': datetime2str(element[9]) if element[9] else None
            })

        return proxies

    def close(self):
        try:
            self._cursor.close()
            self._conn.close()
            logger.debug('closed MySQL connection')
        except Exception as e:
            logger.error(e)
            raise Exception('close MySQL connection failed')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    check_database()

    manager = ProxyDBManager()
    proxies = manager.get_all_valid_proxy(VALID_PROXY_HOUR_THRESHOLD)
    print(proxies)

    proxies = manager.get_all_proxy_for_check(CHECK_PROXY_HOUR_THRESHOL)
    print(proxies)
