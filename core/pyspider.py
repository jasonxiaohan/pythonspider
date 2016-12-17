#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
pyspider
Created on 2016年11月04日
@author: DAIXIAOHAN
"""
from bs4 import BeautifulSoup
import urllib.parse as urlparse
from operator import itemgetter
import hashlib
import time
import _thread
import math
import re
import json
import random
from core.log import log
from core.util import util
from core.db import db
from core.requests import requests
from libs.cls_redis import cls_redis

class pyspider(util,cls_redis,db):

    # 版本号
    __VERSION = "1.0.0"

    # 爬虫爬取每个网页的时间间隔，0表示不延时，单位：秒
    __INTERVAL = 0

    # 爬虫爬取每个网页的超时时间，单位：秒
    __TIMEOUT = 5

    # 爬取失败次数，不想失败重新爬取则设置为0
    __MAX_TRY = 0

    # 并发任务数
    tasknum = 1

    #爬虫开始时间
    time_start = 0

    #当前进程采集成功数
    collect_succ = 0

    #当前进程采集失败数
    collect_fail = 0

    # 爬虫爬取网页所使用的浏览器类型:android、ios、pc、mobile
    __AGENT_ANDROID = "Mozilla/5.0 (Linux; U; Android 6.0.1;zh_cn; Le X820 Build/FEXCNFN5801507014S) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/49.0.0.0 Mobile Safari/537.36 EUI Browser/5.8.015S"
    __AGENT_IOS = ""

    # 要抓取的URL字典
    collect_dict = {}

    # 要抓取的URL列表
    collect_urls = []

    #所有抓取的URL列表
    set_urls = []

    # 要抓取的URL数量
    collect_urls_num = 0

    # 已经爬取的URL数量
    collected_urls_num = 0

    # 提取到的字段数
    fields_num = 0

    export_type = ""
    export_file = ""
    export_conf = ""
    export_table = ""

    # 配置
    configs = {}

    def __init__(self, configs):
        # 是否显示日志
        log.log_show = True

        self.configs = configs
        self.configs["name"] = self.configs["name"] if self.configs["name"] else "pyspider"
        self.configs['proxy'] = self.configs["proxy"] if self.configs.get("proxy") else {}
        # 爬虫爬取时间间隔，单位：秒
        try:
            self.configs["interval"] = self.configs["interval"] if self.configs.get("interval") else self.__INTERVAL
        except KeyError:
            self.configs["interval"] = self.__INTERVAL
        # 爬虫爬取超时时间，单位：秒
        try:
            self.configs["timeout"] = self.configs["timeout"] if self.configs.get("timeout") else self.__TIMEOUT
        except KeyError:
            self.configs["timeout"] = self.__TIMEOUT
        # 爬虫爬取每个网页失败后尝试次数
        try:
            self.configs["max_try"] = self.configs["max_try"] if self.configs.get("max_try") else self.__MAX_TRY
        except KeyError:
            self.configs["max_try"] = self.__MAX_TRY
        try:
            self.configs['max_depth'] = self.configs["max_depth"] if self.configs.get("max_depth") else 0
        except KeyError:
            self.configs["max_depth"] = 0
        try:
            self.configs['max_fields'] = self.configs["max_fields"] if self.configs.get("max_fields") else 0
        except KeyError:
            self.configs["max_fields"] = 0
        # 爬虫爬取网页所使用的随机浏览器类型
        # 爬虫爬取网页时随机使用其中一种浏览器类型，用于破解防采集
        try:
            self.configs["user_header"] = self.configs["user_header"] if self.configs.get("user_header") else []
        except KeyError:
            self.configs["user_header"] = []
        try:
            self.configs["user_header"] = {
                "User-Agent": self.configs["user_agents"][random.randint(0, len(self.configs["user_agents"])-1)]
                if self.configs.get("user_agents") else "Mozilla/5.0"
            }
        except KeyError:
            pass

        # csv、sql、db
        try:
            self.export_type = self.configs["export"]["type"] if self.configs["export"]["type"] else ""
        except KeyError:
            self.export_type = ""
        try:
            self.export_file = self.configs["export"]["file"] if self.configs["export"]["file"] else ""
        except KeyError:
            self.export_file = ""
        try:
            self.export_table = self.configs["export"]["table"] if self.configs["export"]["table"] else ""
        except KeyError:
            self.export_table = ""

        # 是否设置了并发任务数，并且大于1
        try:
            self.tasknum = self.configs["tasknum"]
        except KeyError:
            self.tasknum = 1


    """
        当一个field的内容被抽取到后进行的回调,在此回调中可以对网页中抽取的内容作进一步处理
    """
    def on_extract_field(self, fieldname, data, page):
        return data
    """
    是否从当前页面分析提取URL
    回调函数如果返回false表示不需要再从此网页中发现待爬url
    """
    def on_scan_page(self, page = {}, raw = ""):
        return True
    """
    URL属于列表页
    在爬取到列表页url的内容之后, 添加新的url到待爬队列之前调用
    主要用来发现新的待爬url, 并且能给新发现的url附加数据
    """
    def on_list_page(self, page = {}, raw = ""):
        return True
    """
    放这个位置，可以添加入口页面
    """
    def on_start(self, r):
        return True
    """
    URL属于内容页
    在爬取到内容页url的内容之后, 添加新的url到待爬队列之前调用
    主要用来发现新的待爬url, 并且能给新发现的url附加数据
    """
    def on_content_page(self, page = {}, raw = ""):
        return True

    def start(self):
        try:
            log.log_show = self.configs["log_show"]
        except:
            log.log_show = True
        # 爬虫开始时间
        self.time_start = time.time()
        self.collect_succ = 0
        self.collect_fail = 0
        #检查scan_urls

        if len(self.configs["scan_urls"]) == 0:
            log.error("No scan url to start")
            return False

        for url in self.configs["scan_urls"]:
            if self.is_scan_page(url) == False:
                log.error("Domain of scan_urls (\"{url}\") does not match the domains of the domain name".format(url=url))
                return False
        # 多任务
        if self.tasknum > 1:
            # 清空redis里面的数据
            self.cache_clear()

        # 添加入口URL到队列
        for url in self.configs["scan_urls"]:
            self.add_scan_url(url)
        i = 0

        while self.set_lsize():
            # 抓取页面
            self.collect_page()

            # 多线程下主任务未准备就绪
            if self.tasknum > 1:
                # 主线程采集到两倍于任务数时，生成子任务一起采集
                if self.set_lsize() > self.tasknum*2:
                    i = 1
                    while i < self.tasknum:
                        self.fork_one_task()
                        i+=1
    """
    创建一个子进程
    """
    def fork_one_task(self):
        while self.set_lsize():
            # 如果队列中的网页比任务数2倍多，子任务可以采集，否则等待
            if self.set_lsize() > self.tasknum*2:
                _thread.start_new_thread(self.collect_page, ("threadName", 1))
    """
    根据配置提取HTML代码块中的字段
    @:param confs
    @:param html
    @:param url
    @:param page
    """
    def get_fields(self, confs, html, url, page = {}):
        fields = {}
        # 设置抽取规则,目前默认为beautifulsoup html.parser
        try:
            soup = BeautifulSoup(html, 'html.parser')
        except Exception as e:
            return fields

        for field in confs:
            values = []
            values = soup.select(field["selector"])

            # 检测字典是否有值，并且此字段必须有值
            if len(values) <= 0 and field["required"] == True:
                fields = {}
                break
            # 检测字典是否有值
            if len(values) <= 0:
                fields[field["name"]] = ""
                continue
            # 获取返回结果列表索引值
            if "position" in field:
                values = values[field["position"]]
            else:
                values = values[0]
            # 检测字段是否为获取图片内容
            if values.get("src"):
                value = values.get("src")
            else:
                value = values.get_text()
            data = self.on_extract_field(field["name"], value, page)
            fields[field["name"]] = data.strip()
        if fields:
            tp = tuple(sorted(fields.items(), key=itemgetter(0)))
            return tp
        return fields

    """
    分析提取HTML页面中的字段
    """
    def get_html_fields(self, html, url, page):
        fields = self.get_fields(self.configs["fields"], html, url, page)
        if fields:
            fields_num = self.incr_fields_num()
            if self.configs["max_fields"] != 0 and fields_num > self.configs["max_fields"]:
                return
            # log.info("Result[{fields_num}]: {fields_str}".format(fields_num=fields_num, fields_str=fields))
            # 如果设置了导出选项
            if self.configs["export"]:
                if self.export_type == "csv":
                    util.put_file(self, self.export_file, util.format_csv(self, fields))
                elif self.export_type == "sql":
                    sql = db.insert(self, self.export_table, fields, True)
                    util.put_file(self, self.export_file, sql+";\n")
                elif self.export_type == "db":
                    pass

    """
    爬取页面
    """
    def collect_page(self, threadName = "", delay = 0):
        get_collect_url_num = self.get_collect_url_num()
        log.info("Find pages: {get_collect_url_num} ".format(get_collect_url_num = get_collect_url_num))

        set_lsize = self.set_lsize()
        log.info("Waiting for collect pages: {set_lsize} ".format(set_lsize = set_lsize))

        get_collected_url_num = self.get_collected_url_num()
        log.info("Collected pages: {get_collected_url_num} ".format(get_collected_url_num = get_collected_url_num))

        # 先近先出
        link = self.set_rpop()
        link = self.link_uncompress(link)
        url = link['url']
        # 标记为已爬取网页
        self.incr_collected_url_num(url)
        # 爬取网页开始时间
        page_time_start = time.time()
        html = self.request_url(url, link)
        if not html:
            return False
        #当前正在爬取的网页页面的对象
        page = {
            "url": url,
            "raw": html,
            "request":
            {
                "url": url,
                "method": link["method"],
                "headers": link["headers"],
                "params": link["params"],
                "context_data": link["context_data"],
                "try_num": link["try_num"],
                "max_try": link["max_try"],
                "depth": link["depth"]
            }
        }
        del html

        #是否从当前页面分析提取URL
        #回调函数如果返回false表示不需要再从此网页中发现待爬url
        is_find_url = True
        if link["url_type"] == "scan_page":
            is_find_url = self.on_scan_page(page, page["raw"])
        elif link["url_type"] == "list_page":
            is_find_url = self.on_list_page(page, page["raw"])
        elif link["url_type"] == "content_page":
            is_find_url = self.on_content_page(page, page["raw"])

        # on_scan_page、on_list_page、on_content_page 返回false表示不需要再从此网页中发现待爬url
        if is_find_url:
            # 如果深度没有超过最大深度，获取下一级URL
            if self.configs["max_depth"] == 0 or link["depth"] < self.configs["max_depth"]:
                #分析提取HTML页面中的URL
                try:
                    self.get_html_urls(page["raw"], url, link["depth"]+1)
                except UnicodeDecodeError:
                    pass
        # 如果是内容页，分析提取HTML页面中的字段
        if link["url_type"] == "content_page":
            self.get_html_fields(page["raw"], url, page)
        # 爬虫爬取每个网页的时间间隔，单位：秒
        if self.configs["interval"]:
            time.sleep(self.configs["interval"])

    """
    发现要抓取的网页数量
    """
    def get_collect_url_num(self):
        if self.tasknum > 1:
            count = int(cls_redis.get(self, "collect_urls_num").decode("utf-8"))
        else:
            count = self.collect_urls_num
        return count

    """
    等待爬取网页数量
    """
    def get_collected_url_num(self):
        if self.tasknum > 1:
            count = cls_redis.get(self, "collected_urls_num")
            if count:
                count = int(count.decode("utf-8"))
        else:
            count = self.collected_urls_num
        return count

    """
    是否为入口页面
    """
    def is_scan_page(self, url):
        parse_url = urlparse.urlparse(url)
        if parse_url.netloc == None or parse_url.netloc not in self.configs["domains"]:
            return False
        return True

    """
    """
    def add_scan_url(self, url, options = {}, allowed_repeat = True):
         if self.is_scan_page(url) == False:
             log.error("Domain of scan_urls ("+url+") does not match the domains of the domain name\n")

         link = {}
         link["url"] = url
         link["url_type"] = "scan_page"
         link = self.link_uncompress(link)
         self.set_lpush(link = link,allowed_repeat = allowed_repeat)
         log.debug("Find scan page: {0}".format(url))

    """
    连接对象解压缩
    """
    def link_uncompress(self, link):
        links = {}
        if "url" in link:
            links["url"] = link["url"]
        else:
            links["url"] = ""
        if "url_type" in link:
            links["url_type"] = link["url_type"]
        else:
            links["url_type"] = ""
        if "method" in link:
            links["method"] = link["method"]
        else:
            links["method"] = "get"
        if "headers" in link:
            links["headers"] = link["headers"]
        else:
            links["headers"] = {}
        if "params" in link:
            links["params"] = link["params"]
        else:
            links["params"] = {}
        if "context_data" in link:
            links["context_data"] = link["context_data"]
        else:
            links["context_data"] = ""
        if "proxy" in link:
            links["proxy"] = link["proxy"]
        else:
            links["proxy"] = self.configs["proxy"]
        if "try_num" in link:
            links["try_num"] = link["try_num"]
        else:
            links["try_num"] = 0
        if "max_try" in link:
            links["max_try"] = link["max_try"]
        else:
            links["max_try"] = self.configs["max_try"]
        if "depth" in link:
            links["depth"] = link["depth"]
        else:
            links["depth"] = 0
        return links

    """
    从列表左侧插入
    """
    def set_lpush(self, link = {}, allowed_repeat = False):
        if len(link) <=0:
            return False
        url = link["url"]
        status = False
        if self.tasknum > 1:
            key = "collect_urls-"+self.md5(url)
            exists = cls_redis.exists(self, key)
            if not exists:
                # 待爬取网页记录数加一
                cls_redis.incr(self, "collect_urls_num")
                # 先标记为待爬取网页
                cls_redis.set(self, key, time.time())
                # 入队列
                link = json.dumps(link)
                cls_redis.lpush(self, "collect_queue", link)
                status = True
        else:
            key = self.md5(url)
            if key not in self.set_urls:
                self.collect_urls_num += 1
                self.collect_urls.append(key)
                self.set_urls.append(key)
                self.collect_dict[key] = link
                status = True

        return status

    """
    从列表右侧插入
    """
    def set_rpush(self, link = {}, allowed_repeat = False):
        if len(link) <= 0:
            return False
        url = link["url"]
        status = False

        # 多线程处理
        if self.tasknum > 1:
            key = "collect_urls-"+self.md5(url)
            exists = cls_redis.exists(self, key)
            if not exists:
                # 待爬取网页记录数加一
                cls_redis.incr(self, "collect_urls_num")
                # 先标记为待爬取网页
                cls_redis.set(key, time.time())
                # 入队列
                link = json.dumps(link)
                cls_redis.rpush(self, "collect_queue", link)
                status = True
        else:
            key = self.md5(url)
            if key not in self.set_urls:
                self.collect_urls.append(key)
                self.set_urls.append(key)
                self.collect_dict[key] = link
                status = True
        return status

        pass

    """
    从队列右侧取出
    """
    def set_rpop(self):
        if self.tasknum > 1:
            link = cls_redis.rpop(self, "collect_queue")
            link = json.loads(link.decode("utf-8"))
            return link
        else:
            if len(self.collect_urls):
                key = self.collect_urls.pop(0)
                return self.collect_dict[key]
    """
    队列长度
    """
    def set_lsize(self):
        if self.tasknum > 1:
            lsize = cls_redis.llen(self, "collect_queue")
            if lsize:
                lsize = int(lsize)
            else:
                lsize = 0
        else:
            lsize = len(self.collect_urls)
        return lsize
    """
    添加已爬取网页标记
    """
    def incr_collected_url_num(self, url):
        if self.tasknum > 1:
            cls_redis.incr(self, "collected_urls_num")
        else:
            self.collected_urls_num+=1

    """
    对字符串进行md5加密
    """
    def md5(self, str):
        m = hashlib.md5(str.encode(encoding="gb2312"))
        md5value = m.hexdigest()
        return md5value

    """
    下载网页，得到网页内容
    """
    def request_url(self, url="", link={}):
        time_start = time.time()
        method = link["method"] if link.get("method") else "get"
        params = link["params"] if link.get("params") else {}
        # 是否设置了代理
        r = requests(self.configs["timeout"])
        r.set_header(self.configs["user_header"])
        self.on_start(r)
        if link.get("headers"):
            for key in link["headers"]:
                r.add_header(key, link["headers"][key])
        if self.configs.get("proxy"):
            r.set_proxies(self.configs["proxy"])
        if method == "get":
            html = r.get(url, params)
        else:
            html = r.post(url, params)
        http_code = html["status"]
        if http_code != 200:
            # 如果是301、302跳转，抓取跳转后的网页内容
            if http_code == 301 or http_code == 302:
                pass
            else:
                if http_code == 407:
                    # 扔到字典头部去，继续采集
                    self.set_rpush(link)
                    log.error("Failed to download page {url}".format(url=url))
                elif http_code in ["0","403","502","503","429"]:
                    # 采集次数加一
                    link["try_num"]+=1
                    # 抓取次数 小于 允许抓取失败次数
                    if link["try_num"] < link["max_try"]:
                        # 扔到字典头部去，继续采集
                        self.set_rpush(link)
                    log.error("Failed to download page {url}, retry({try_num})".format(url=url,try_num=link["try_num"]))
                else:
                    log.error("Failed to download page {url}".format(url=url))
                self.collect_fail+=1
                return False

        # 爬取页面耗时时间
        time_run = math.trunc(time.time() - time_start)
        log.debug("Success download page {url} in {time_run} s".format(url=url, time_run=time_run))
        self.collect_succ += 1
        return html['content']

    """
    分析提取HTML页面中的URL
    @:param html HTML内容
    @:param collect_url 抓取的URL，用来拼凑完整页面的URL
    """
    def get_html_urls(self, html, collect_url, depth = 0):
        """
        过滤和拼凑URL
        去除重复的RUL
        """
        soup = BeautifulSoup(html, "html.parser")
        urls = set()
        for x in soup.find_all('a'):  #返回所有有匹配的列表
            link = x.get('href')
            if not link:
                continue
            urls.add(link)
        if len(urls) == 0:
            return False
        # 过滤过后的URL
        urls_ = set()
        for url in urls:
            url = url.strip()
            if url == "":
                continue
            val = self.fill_url(url, collect_url)
            if val:
                urls_.add(val)
        del urls
        """把抓取到的URL放入列表"""
        for url in urls_:
            # 把当前页当做找到的url的Referer页
            options = {"headers": {"Referer": collect_url}}
            self.add_url(url, options, depth)

    """
    获得完整的连接地址
    @:param url 要检查的URL
    @:param collect_url 从那个URL页面得到上面的URL
    """
    def fill_url(self, url, collect_url):
        collect_url = collect_url.strip()
        # 排除javascrip的连接
        if re.match("^javascript:.*?", url, re.M | re.I):
            return False
        url_parse = urlparse.urlparse(collect_url)
        if url_parse.scheme == "" or url_parse.netloc == "":
            return False
        scheme = url_parse.scheme
        domain = url_parse.netloc
        path = url_parse.path if url_parse.path else ""
        base_url_path = domain+path
        base_url_path = re.sub("\/([^\/]*)\.(.*)$", "/", base_url_path)
        base_url_path = re.sub("\/$", "", base_url_path)

        i = path_step = 0
        dstr = pstr = ""
        pos = url.find("#")
        if pos > 0:
            # 去掉#后面的字符串
            url = url[0:pos]
        # 京东变态的都是//www.jd.com/1234.html
        if url[0:2] == "//":
            url = url.replace("//", "")
        # 1234.html
        elif url[0:1] == "/":
            url = domain+url
        # ./1234.html、../1234.html 这种类型
        elif url[0:1] == ".":
            if url[2:3]:
                return False
            else:
                urls = url.split("/")
                for u in urls:
                    if u == "..":
                        path_step+=1
                    elif i < len(urls)-1:
                        pass
                    else:
                        dstr = dstr+urls[i]
                    i+=1
                urls = base_url_path.split("/")
                if len(urls) <= path_step:
                    return False
                else:
                    pstr = ""
                    for i in len(urls) - path_step:
                        pstr = pstr+urls[i]+"/"
                    url = pstr+dstr
        else:
            if url[0:7].lower() == "http://":
                url = re.sub(r"([a-zA-Z]*)://", "", url)
                scheme = "http"
            elif url[0:8].lower() == "https://":
                url = re.sub(r"([a-zA-Z]*)://", "", url)
                scheme = "https"
            else:
                url = base_url_path+"/"+url
        # 两个 / 或以上的替换成一个
        url = re.sub(r"/{1,}", "/", url)
        url = scheme+"://"+url
        url_parse = urlparse.urlparse(url)
        domain = url_parse.netloc if url_parse.netloc else domain
        # 如果host不为空，判断是不是要抓取的域名
        if url_parse.netloc:
            # 排除非域名下的url以提高爬取速度
            #if url_parse.netloc not in self.configs["domains"]:
            #    return False
            pass
        return url

    """
    是否为列表页
    @:param 检查URL
    """
    def is_list_page(self, url):
        result = False
        if self.configs["list_url_regexes"]:
            for regex in self.configs["list_url_regexes"]:
                if re.match(regex, url, re.M|re.I):
                    result = True
                    break
        return result

    """
    检查是否为内容页
    """
    def is_content_page(self, url):
        result = False
        if self.configs["content_url_regexes"]:
            for regex in self.configs["content_url_regexes"]:
                if re.match(regex, url, re.M|re.I):
                    result = True
                    break
        return result

    """
    一般在on_scan_page 和 on_list_page 回调函数中调用，用来往待爬队列中添加url
    """
    def add_url(self, url, options = {}, depth = 0):
        # 投递状态
        status = False
        link = options
        link["url"] = url
        link["depth"] = depth
        link = self.link_uncompress(link)
        # 列表页
        if self.is_list_page(url):
            log.debug("Find list page: {url}".format(url=url))
            link['url_type'] = 'list_page'
            status = self.set_lpush(link)
        # 内容页
        if self.is_content_page(url):
            log.debug("Find content page: {url}".format(url=url))
            link['url_type'] = 'content_page'
            status = self.set_lpush(link)
        return status

    """
    提取到的field数目加一
    """
    def incr_fields_num(self):
        self.fields_num += 1
        fields_num = self.fields_num
        return fields_num

    """
    清空Redis里面上次爬取的采集数据
    """
    def cache_clear(self):
        #  删除队列
        cls_redis.delete(self, "collect_queue")
        # 删除采集到的field数量
        cls_redis.delete(self, "fields_num")
        # 抓取和抓取到数量
        cls_redis.delete(self, "collect_urls_num")
        cls_redis.delete(self, "collected_urls_num")

        # 删除等待采集网页缓存
        keys = cls_redis.keys(self, "collect_urls-*")
        for key in keys:
            cls_redis.delete(self, key)
