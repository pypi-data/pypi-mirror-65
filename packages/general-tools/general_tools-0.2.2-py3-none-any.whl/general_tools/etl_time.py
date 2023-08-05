#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright (C)2018 SenseDeal AI, Inc. All Rights Reserved
File: .py
Author: xuwei
Email: weix@sensedeal.ai
Last modified: date
Description:
'''

import datetime
import time


class TimeEtl(object):

    @classmethod
    def ge_now(cls):
        return datetime.datetime.now()

    @classmethod
    def time_str(cls, _now):
        _str_now = _now.strftime("%Y-%m-%d %H:%M:%S")
        return _str_now

    @classmethod
    def time_date(cls, _now):
        _str_now = _now.strftime("%Y-%m-%d")
        return _str_now

    @classmethod
    def time_clock(cls, _now):
        _str_now = _now.strftime("%H:%M:%S")
        return _str_now

    @classmethod
    def time_stamp(cls, _now):
        un_time = time.mktime(_now.timetuple())
        return int(un_time)

    @classmethod
    def str_time(cls, _str):
        _time = datetime.datetime.strptime(_str, "%Y-%m-%d %H:%M:%S")
        return _time

    @classmethod
    def str_time_stamp(cls, _str):
        _time = cls.str_time(_str)
        _time_stamp = cls.time_stamp(_time)
        return _time_stamp

    @classmethod
    def date_time(cls, _str):
        _time = datetime.datetime.strptime(_str, "%Y-%m-%d")
        return _time

    @classmethod
    def stamp_time(cls, _stamp):
        _dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(_stamp))
        return _dt

    @classmethod
    def before_day(cls, _now, _day):
        _time = (_now - datetime.timedelta(days=_day)).strftime("%Y-%m-%d")
        return _time

    @classmethod
    def after_day(cls, _now, _day):
        _time = (_now + datetime.timedelta(days=_day)).strftime("%Y-%m-%d")
        return _time


etl_time = TimeEtl()

if __name__ == '__main__':
    _now = datetime.datetime.now()
    _str_time = TimeEtl.time_stamp(_now)
    # print(_str_time)
    #
    _time = TimeEtl.stamp_time(_str_time)
    print(_time)
