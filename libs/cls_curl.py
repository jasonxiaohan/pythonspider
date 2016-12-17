#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Worker多进程操作类
Created on 2016年11月03日
文件储存处理
@author: DAIXIAOHAN
"""
import gzip
import http.cookiejar
import urllib.request
import urllib.parse as urlparse

class cls_curl:
    __headers = {}
    def __init__(self):
        pass

    """
    设置Headers
    @:param string headers
    @:return void
    """
    def set_header(self, headers):
        self.__headers = headers

    """
    下载远程url链接数据
    @:param string type type、post
    @:param string url
    @:param dict fields
    @:return html
    """
    def http_request(self, url, type_, fields):
        opener = self.getOpener()
        if(type_.upper() == "GET" or type_ is None):
            url = url+"&{0}" if url.find("?") > 0 else url+"?{0}".format(urlparse.urlencode(fields))
            op = opener.open(url)
        else:
            postdata = urlparse.urlencode(fields).encode()
            op = opener.open(url, postdata)
        #读取html页面
        data = op.read()
        data = self.unizp(data)
        return data

    def getOpener(self):
        cj = http.cookiejar.CookieJar()
        pro = urllib.request.HTTPCookieProcessor(cj)
        opener = urllib.request.build_opener(pro)
        header = []
        for key,value in self.__headers:
            elem = (key,value)
            header.append(elem)
        opener.addheaders = header
        return opener

    """
    解压
    """
    def unizp(self, data):
        try:
            data = gzip.decompress(data)
        except:
            pass
        return data

