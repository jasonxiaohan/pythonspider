#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
from operator import itemgetter
from core.pyspider import  pyspider
from core.requests import requests
from core.util import util
from config import inc_config
from libs.cls_redis import cls_redis
import urllib.parse as urlparse
import os
import json

filepath = os.path.split(os.path.realpath(__file__))[0]

# 马蜂窝
configs = {
   "name": "搜狐汽车",
   "log_show": True,
   # "proxy": {"http": "http://H30244YAX2L7282D:E5AF4CCDF2C72F87@proxy.abuyun.com:9010"},
   "tasknum": 1,
   "timeout": 100,
   "interval": 1,
   "domains": ["db.auto.sohu.com"],
   "scan_urls": ["http://db.auto.sohu.com/"], #定义入口地址
   "list_url_regexes": ["http://db.auto.sohu.com/([a-zA-Z-]+).shtml"],
   "content_url_regexes": ["http://db.auto.sohu.com/([a-zA-Z0-9]+)-\d+/\d+$"],  #详情页
   "max_try": 1,
   "user_agents": ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"," Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G34 Safari/601.1"],
   "export": {"type": "csv", "file": filepath+util().separator()+"data"+util().separator()+"sohu_car.txt"},  # 导出数据类型
   # "export": {"type": "sql", "table": "qiushibaike", "file": filepath+util().separator()+"data"+util().separator()+"qiushibaike.sql"},  # 导出数据类型
   "fields":[
      # {"name": "name", "selector": "title", "required": True},
      {"name": "type", "selector": "title", "required": True},
      {"name": "url", "selector": "title", "required": False},   # 这里随便设置，on_extract_field回调里面会替换
   ]
}

# 替换集合
spider = pyspider(configs)
def on_extract_field(fieldname, data, page):
    if fieldname == "url":
        data = page["url"]
    elif fieldname == "type":
        idList = re.findall(re.compile('http://db.auto.sohu.com/[a-zA-Z-]+\d+/([0-9]+)'),page["url"])
        for x in idList:
            url = "http://db.auto.sohu.com/api/model/select/trims_"+x+".json"
            html = spider.request_url(url)
            if html:
                try:
                    jsons = json.loads(html.decode("utf-8"))
                except Exception as e:
                    jsons = json.loads(html)
                result = [trims for row in jsons["trimyears"]
                          for trims in row["trims"]
                          ]
                data = ""
                for r in result:
                    data += str(x)+"$"+str(r["tid"]) + "$" + r["tname"] + "|"
                return data

    data=data.replace('\n', "").replace('\t', "").replace(" ", "")
    return data

spider.on_extract_field = on_extract_field
spider.start()



