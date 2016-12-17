import urllib.parse as urlparse
from bs4 import BeautifulSoup
import re
from operator import itemgetter
from libs.cls_curl import cls_curl
from core.pyspider import  pyspider
from core.requests import requests
from core.util import util
from config import inc_config
from libs.cls_redis import cls_redis
import urllib.parse as urlparse
import inspect
import time
import math
import os
import json
import threading
import _thread
import random
filepath = os.path.split(os.path.realpath(__file__))[0]

# 马蜂窝
configs = {
   "name": "马蜂窝",
   "log_show": True,
   "proxy": {"http": "http://H30244YAX2L7282D:E5AF4CCDF2C72F87@proxy.abuyun.com:9010"},
   "tasknum": 1,
   "timeout": 100,
   "interval": 1,
   "domains": ["www.mafengwo.cn"],
   "scan_urls": ["http://www.mafengwo.cn/travel-scenic-spot/mafengwo/10088.html"], #定义入口地址
   "list_url_regexes": ["http://www.mafengwo.cn/mdd/base/list/pagedata_citylist\?page=\d+", "http://www.mafengwo.cn/gonglve/ajax.php\?act=get_travellist\&mddid=\d+"],
   "content_url_regexes": ["http://www.mafengwo.cn/i/\d+.html"],  #详情页
   "max_try": 1,
   "user_agents": ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"," Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G34 Safari/601.1"],
   "export": {"type": "csv", "file": filepath+util().separator()+"data"+util().separator()+"mafengwo.txt"},  # 导出数据类型
   # "export": {"type": "sql", "table": "qiushibaike", "file": filepath+util().separator()+"data"+util().separator()+"qiushibaike.sql"},  # 导出数据类型
   "fields":[
      {"name": "name", "selector": "h1", "required": True},
      {"name": "city", "selector": "div.relation_mdd", "required": False},
      {"name": "date", "selector": "li.time", "required": False},
      {"name": "day", "selector": "li.day", "required": False},
      {"name": "price", "selector": "li.cost", "required": False},
      {"name": "people", "selector": "li.people", "required": False},
      {"name": "url", "selector": "h1", "required": False},   # 这里随便设置，on_extract_field回调里面会替换
   ]
}

# 替换集合
transforms = [('出发时间', ''), ('出行天数', ''), ('人物', ''), ('人均费用', '')]
spider = pyspider(configs)
def on_extract_field(fieldname, data, page):
    for transform in transforms:
       data = data.replace(*transform)
    if fieldname == "url":
        data = page["url"]
    data=data.replace('\n', "").replace('\t', "").replace(" ", "")
    return data
def on_start(r):
    r.add_header("Referer", "http://www.mafengwo.cn/mdd/filter-tag-116.html")
    return r

def on_scan_page(page = {},raw = ""):
   for i in range(5,6):
      #  全国热点城市
      url = "http://www.mafengwo.cn/mdd/base/list/pagedata_citylist?page=%s"%i
      options = {
         "url_type":url,
         "method":"post",
         "params":{
            "mddid":21536,
            "page":i
         }
      }
      spider.add_url(url, options)
   return True
def on_list_page(page = {}, content=""):
   if re.search("pagedata_citylist", page["request"]["url"], re.M | re.I):
      data = json.loads(content)
      html = data["list"]
      urlList = re.findall(re.compile('<a href="/travel-scenic-spot/mafengwo/(.*?).html"'), html)
      for id in urlList:
          url = "http://www.mafengwo.cn/gonglve/ajax.php?act=get_travellist&mddid=%s"%id
          options = {
             "url_type": url,
             "method": "post",
             "params":{
                "mddid": 15325,#searchObj.groups()[0],
                "pageid": "mdd_index",
                "sort": 1,
                "cost": 0,
                "days": 0,
                "month": 0,
                "tagid": 0,
                "page": 1,
             }
          }
          spider.add_url(url, options)
   #  文章列表页
   else:
      data = json.loads(content)
      html = data["list"]
      if page["request"]["params"]["page"] == 1:
         data_page = data["page"].strip()
         countObj = re.search('<span class="count">共<span>(.*?)</span>页', data_page, re.M | re.I)
         if countObj:
             for i in range(0, int(countObj.groups()[0])+1):
                v = page['request']['params']['mddid']
                url = "http://www.mafengwo.cn/gonglve/ajax.php?act=get_travellist&mddid={v}&page={i}".format(v=v, i=i)
                options = {
                   "url_type": url,
                   "method": "post",
                   "params":{
                      "mddid": v,
                      "pageid": 'mdd_index',
                      "sort": 1,
                      "cost": 0,
                      "days": 0,
                      "month": 0,
                      "tagid": 0,
                      "page": i
                   }
                }
                spider.add_url(url, options)
      urlList = re.findall(re.compile('<a href="/i/(.*?).html" target="_blank">'), html)
      for id in urlList:
         url = "http://www.mafengwo.cn/i/{id}.html".format(id=id)
         spider.add_url(url)

spider.on_start = on_start
spider.on_extract_field = on_extract_field
spider.on_scan_page = on_scan_page
spider.on_list_page = on_list_page
spider.start()

