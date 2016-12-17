#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import gzip
import http.cookiejar
import urllib.request
import urllib.parse as urlparse
from bs4 import BeautifulSoup
import socket

"""
requests  请求类文件
Created on 2016年11月09日
@author: DAIXIAOHAN
"""
class requests:

    # 版本号
    VERSION = "1.0.0"
    error= ""
    __headers = {}
    # 超时时间
    # 代理信息
    proxies = {}
    content = ""
    status_code = 0

    def __init__(self, timeout=10):
        # 下载超时时间
        socket.setdefaulttimeout(timeout)

    """
    get方式下载
    """
    def get(self, url, fields = {}):
        return self.http_client(url, "get", fields)
    """
    post方式下载
    """
    def post(self, url, fields = {}):
        try:
            return self.http_client(url, "post", fields)
        except (ValueError):
            pass

    def http_client(self, url = '', method = 'GET', fields = {}):
        method = method.upper()
        if self._is_url(url) is False:
            self.error = "You have requested URL ({url}) is not a valid HTTP address".format(url=url)
            return {"status": 500, "content": ""}
        # 如果是get方式，直接拼接一个url出来
        if method == "GET" and not fields:
            url = url + "&{0}" if url.find("?") > 0 else url + "?{0}".format(urlparse.urlencode(fields))
        parse_url = urlparse.urlparse(url)
        if parse_url.netloc == "" or parse_url.scheme not in ["http","https"]:
            self.error = "No connection adapters were found for '{url}'".format(url=url)
            return {"status": 404, "content": ""}
        scheme = parse_url.scheme
        domain = parse_url.netloc

        opener = self.getOpener()
        try:
            if (method.upper() == "GET" or method is None):
                url = url + "&{0}" if url.find("?") > 0 else url + "?{0}".format(urlparse.urlencode(fields))
                op = opener.open(url)
            else:
                postdata = urlparse.urlencode(fields).encode()
                op = opener.open(url, postdata)
        except Exception as e:
            if "HTTP Error 503" in str(e):
                return {"status": 503, "content": ""}
            elif "HTTP Error 403" in str(e):
                return {"status": 403, "content":""}
            return {"status": 502, "content": ""}

        #读取html页面
        try:
            content = op.read()
        except:
            return {"status": 407, "content": ""}
        html = ""
        try:
            html = gzip.decompress(content)
            html = html.decode('gbk')
        except (Exception, OSError) as e:
            try:
                html = content.decode('utf-8')
            except Exception:
                pass
        # try:
        #     # soup = BeautifulSoup(html, 'html.parser')  # "html.parser",from_encoding='GBK'
        #     pass
        # except Exception as e:
        #     print("错误："+str(e))
        status_code = self.get_http_status(op.reason)
        info = {"status": status_code, "content": html}
        return info

    """
    简单的判断一下是否为一个URL链接
    """
    def _is_url(self, url):
        if re.match("^((https?|ftp)://|(www|ftp)\.)[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+([/?].*)?$", url):
            return True
        return False

    def getOpener(self):
        cj = http.cookiejar.CookieJar()
        pro = urllib.request.HTTPCookieProcessor(cj)
        if self.proxies:
            proxy_handler = urllib.request.ProxyHandler(self.proxies)
            opener = urllib.request.build_opener(pro, proxy_handler)
        else:
            opener = urllib.request.build_opener(pro)
        header = []
        for key,value in self.__headers.items():
            elem = (key,value)
            header.append(elem)
        opener.addheaders = header
        return opener

    """
    设置Headers
    @:param string headers
    @:return void
    """
    def set_header(self, headers):
        self.__headers = headers

    """
    设置Headers
    """
    def add_header(self, key, value):
        if key not in self.__headers:
            self.__headers[key] = value

    def get_http_status(self, http_status):
        codes = {"OK": 200}
        return codes[http_status]

    """
    设置代理
    """
    def set_proxies(self, proxies):
        self.proxies = proxies
