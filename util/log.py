#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

from config import LOG_LEVEL, LOG_FILE_USE, LOG_STREAM_USE, LOG_FILE


def log_init():
    _level = _log_level(LOG_LEVEL)
    _handlers = []

    if LOG_FILE_USE:
        _handlers.append(_FileHandler(_level))

    if LOG_STREAM_USE:
        _handlers.append(_StreamHandler(_level))

    logging.basicConfig(level=_level, handlers=_handlers)


def _FileHandler(level):
    file_name = str(Path(__file__).parent.parent / Path('log') / Path(LOG_FILE))
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

    file_handler = TimedRotatingFileHandler(filename=file_name, when='D', interval=1, backupCount=15)

    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    file_handler.suffix = '%Y%m%d.log'

    return file_handler


def _StreamHandler(level):
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

    stream_handler = logging.StreamHandler()

    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    return stream_handler


def _log_level(level):
    return {
        'CRITICAL': logging.CRITICAL,
        'FATAL': logging.FATAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'WARN': logging.WARN,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'NOTSET': logging.NOTSET,
    }[level]
