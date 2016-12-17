import urllib.parse as urlparse
from bs4 import BeautifulSoup
import re
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
import threading
import _thread
import random
filepath = os.path.split(os.path.realpath(__file__))[0]
configs = {
   "name": "马蜂窝",
   "proxy": "",
   "tasknum": 5,
   "domains": ["www.mafengwo.cn"],
   "scan_urls": ["http://www.mafengwo.cn/travel-scenic-spot/mafengwo/10088.html"], #定义入口地址
   "list_url_regexes": ["http://www.mafengwo.cn/mdd/base/list/pagedata_citylist\?page=\d+", "http://www.mafengwo.cn/gonglve/ajax.php\?act=get_travellist\&mddid=\d+"], # 列表页
   "content_url_regexes": ["http://www.mafengwo.cn/i/\d+.html"], # 详情页
   "export": {"type": "db","table":"mafengwo_content"}, #导出数据类型
   "fields":[
      {"name": "title", "selector": "h1", "required": True},
      {"name": "desc", "selector": ".l-topic > p", "required": False},
      {"name": "img", "selector": ".banner > img", "required": False},
      {"name": "tiyan", "selector": ".sub-tit", "required": True},
      {"name": "category", "selector": ".crumb", "required": True},
   ]
}

configs = {
   "name": "房天下",
   "proxy": "",
   "tasknum": 1,
   "domains": ["office.fang.com"],
   "scan_urls": ["http://office.fang.com/zu/house/c13-d18-kw%d6%d0%b9%d8%b4%e5/"], #定义入口地址
   "list_url_regexes": ["http://office.fang.com/zu/house/c13-d18-i3[0-9]+-kw%d6%d0%b9%d8%b4%e5/"],
   "content_url_regexes": ["http://office.fang.com/zu/3_\d+.html"],  #详情页
   "export": {"type": "csv", "file": filepath+"\data\data000001.txt"},  # 导出数据类型
   "fields":[
      {"name": "title", "selector": "h1", "required": True},
      {"name": "mobile", "selector": "#mobilecode", "required": False},
      {"name": "username", "selector": "#agentname", "required": False},
   ]
}
# 也买酒
configs = {
   "name": "也买酒",
   "proxy": "",
   "tasknum": 1,
   "timeout": 5,
   "domains": ["list.yesmywine.com"],
   "scan_urls": ["http://list.yesmywine.com/z2/"], #定义入口地址
   "list_url_regexes": ["http://list.yesmywine.com/z2-p[0-9]+/"],
   "content_url_regexes": ["http://www.yesmywine.com/goods/\d+.html"],  #详情页
   "export": {"type": "csv", "file": filepath+util().separator()+"data"+util().separator()+"data000001_yesmywine.txt"},  # 导出数据类型
   "fields":[
      {"name": "title", "selector": "h1", "required": True},
      {"name": "price", "selector": "li.w560", "required": False},
      {"name": "crumb", "selector": "div.crumb", "required": False},
      {"name": "sezhe", "selector": "span.sezhe", "required": False},
   ]
}

# 糗事百科
configs_bak = {
   "name": "糗事百科",
   "log_show": True,
   "proxy": {},
   "tasknum": 1,
   "domains": ["qiushibaike.com","www.qiushibaike.com"],
   "scan_urls": ["http://www.qiushibaike.com/"], #定义入口地址
   "list_url_regexes": ["http://www.qiushibaike.com/8hr/page/\d+/\?s=\d+"],
   "content_url_regexes": ["http://www.qiushibaike.com/article/\d+"],  #详情页
   "max_try": 1,
   "user_agents": ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"," Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G34 Safari/601.1"],
   # "export": {"type": "csv", "file": filepath+util().separator()+"data"+util().separator()+"qiushibaike.txt"},  # 导出数据类型
   "export": {"type": "sql", "table": "qiushibaike", "file": filepath+util().separator()+"data"+util().separator()+"qiushibaike.sql"},  # 导出数据类型
   "fields":[
      {"name": "title", "selector": "div.content", "required": True},
      {"name": "author", "selector": "div.author > a > h2", "required": False},
      {"name": "headimg", "selector": "div.author > a > img", "required": False},
      {"name": "url", "selector": "div.content", "required": False},   # 这里随便设置，on_extract_field回调里面会替换
   ]
}

# 马蜂窝
configs = {
   "name": "马蜂窝",
   "log_show": True,
   "proxy": {},
   "tasknum": 1,
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
      {"name": "city", "selector": "div.relation_mdd", "required": True},
      {"name": "date", "selector": "li.time", "required": True},
      {"name": "url", "selector": "h1", "required": False},   # 这里随便设置，on_extract_field回调里面会替换
   ]
}

spider = pyspider(configs)
# head = {
#     'Connection': 'Keep-Alive',
#     'Accept': 'text/html, application/xhtml+xml, */*',
#     'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
# }
#
# header = []
# for key,value in head.items():
#    elem = (key,value)
#    header.append(elem)
#
# print(header)
# html = spider.request_url("http://www.qiushibaike.com/article/118035429",{"method":"get","params":{},"headers":{}})
# title = html.select("div.author > a > img")
# print(title)
# exit()
"""  也买酒网"""
def on_extract_field(fieldname, data,page):
    if fieldname == "tiyan":
       pattern = re.compile(r'\d+')
       dict = pattern.findall(data)
       if len(dict) > 0:
          return dict[0]
    elif fieldname == "price":
        data = data.replace("您的专享价:", "").replace("¥", "").strip('\n')
    elif fieldname == "crumb":
        pass
        # 把当前内容页URL替换上面的field
    elif fieldname == "url":
        data = page["url"]
    data=data.replace('\n', "").replace('\t', "").replace(" ", "")
    return data
def on_start(r):
    r.add_header("Referer", "http://www.mafengwo.cn/mdd/filter-tag-116.html")
    return r

def on_scan_page(page = {},raw = ""):
   for i in range(0,298):
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
spider.on_start = on_start
spider.on_extract_field = on_extract_field
spider.on_scan_page = on_scan_page
spider.start()
