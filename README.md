pythonspider -- PYTHON蜘蛛爬虫框架

下面以马蜂窝为例, 来看一下我们的爬虫长什么样子:

```
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

spider = pyspider(configs)
spider.start()
```
爬虫的整体框架就是这样, 首先定义了一个configs字典, 里面设置了待爬网站的一些信息, 然后通过调用spider = phpspider(configs)和spider.start()来配置并启动爬虫.

