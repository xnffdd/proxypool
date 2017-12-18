#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from importlib import import_module


def load_object(path):
    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError("Error loading object '%s': not a full path" % path)

    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError("Module '%s' doesn't define any object named '%s'" % (module, name))

    return obj


def get_current_time_str():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def datetime2str(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    print(get_current_time_str())
    now = datetime.datetime.now()
    print(datetime2str(now))
