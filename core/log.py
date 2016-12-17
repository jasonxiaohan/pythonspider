#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time

"""
log  记录日志
Created on 2016年11月06日
@author: DAIXIAOHAN
"""

class log:
    log_show = False
    def error(msg):
        out_sta = "\033[1;31;40m"
        out_end = "\033[0m"
        log().msg(msg, "error", out_sta, out_end)
        return
    def debug(msg):
        out_sta = "\033[1;31;36m"
        out_end = "\033[0m"
        log().msg(msg, "debug", out_sta, out_end)
        return
    def info(msg):
        log().msg(msg, "info", "", "")
    def msg(self, msg, log_type, out_sta, out_end):
        msg = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+" "+log_type+" " + msg +"\n"
        if self.log_show:
            print(out_sta)
            print(msg)
            print(out_end)
