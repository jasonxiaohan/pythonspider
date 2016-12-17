#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
pyspider
Created on 2016年11月14日
@author: DAIXIAOHAN
PythonSpider Redis操作类文件
"""

import redis
from config import inc_config
from core.log import log

class cls_redis:
    # redis链接标识符号
    redis = None
    # redis配置字典
    rd_configs = {}
    # 默认redis前缀
    prefix = "pythonspider"
    error = ""

    def __init__(self):
        log.log_show = True

    def init(self):
        rd_configs = self.rd_configs if self.rd_configs else self.__get_default_config()
        if not rd_configs:
            self.error = "You not set a config dict for connect."
            return False
        # 如果当前链接标识符为空，或者ping不通，就close重新打开
        pool = redis.ConnectionPool(host=rd_configs["host"], port=rd_configs["port"], db=rd_configs["db"], password=rd_configs["pass"])
        self.redis = redis.Redis(connection_pool=pool)
        if not self.redis:
            self.error = "Unable to connect to redis server"
            self.redis = None
            return False
        return self.redis

    """
    get
    @:param key
    """
    def get(self, key):
        self.init()
        try:
            if self.redis:
                return self.redis.get(key)
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
    """
    set
    @:param key 键
    @:param value 值
    @:param expire 过期时间，单位：秒
    """
    def set(self, key, value, expire=0):
        self.init()
        try:
            if self.redis:
                if expire > 0:
                    return self.redis.setex(key, value, expire)
                else:
                    return self.redis.set(key, value)
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None

    """
    setnx
    @:param key 键
    @:param value 值
    @:param expire 过期时间，单位：秒
    """
    def setnx(self, key, value, expire=0):
        self.init()
        try:
            if expire > 0:
                return self.redis.set(key, value, ex=expire, nx=True)
            else:
                return self.redis.setnx(key, value)
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
    delete 删除数据
    @:param key
    """
    def delete(self, key):
        self.init()
        try:
            if self.redis:
                return self.redis.delete(key)
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
    type 返回值的类型
    """
    def type(self, key):
        self.init()
        try:
            if self.redis:
                return self.redis.type(key).decode("utf-8")
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
    incr 名称为key的string增加integer，integer为0则增1
    """
    def incr(self, key, integer=0):
        self.init()
        try:
            if self.redis:
                if integer:
                    return self.redis.incrby(key, integer)
                else:
                    return self.redis.incr(key)
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
    decr 名称为key的string减少integer，integer为0则减1
    """
    def decr(self, key, integer=0):
        self.init()
        try:
            if self.redis:
                if integer:
                    return self.redis.decrby(key, integer)
                else:
                    return self.redis.decr(key)
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
    append名称为key的string的值附加value
    """
    def append(self, key, value):
        self.init()
        try:
            if self.redis:
                return self.redis.append(key, value)
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
    dbsize 返回当前数据库中key的数目
    """
    def dbsize(self):
        self.init()
        try:
            if self.redis:
                return self.redis.dbsize()
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
    flushdb 删除当前选择数据中的所有key
    """
    def flushdb(self):
        self.init()
        try:
            if self.redis:
                return self.redis.flushdb()
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
    flushall 删除所有数据库中的所有key
    """
    def flushall(self):
        self.init()
        try:
            if self.redis:
                return self.redis.flushall()
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
    info 提供服务器的信息和统计
    """
    def info(self):
        self.init()
        try:
            if self.redis:
                return self.redis.info()
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
    lpush 将数据从左边压入
    @:param key 键
    @:param value 值
    """
    def lpush(self, key, value):
        self.init()
        try:
            if self.redis:
                return self.redis.lpush(key, value)
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
   rpush 将数据从右侧压入
    """
    def rpush(self, key, value):
        self.init()
        try:
            if self.redis:
                return self.redis.rpush(key, value)
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
    lpop 从左边弹出数据，并删除数据
    """
    def lpop(self, key):
        self.init()
        try:
            if self.redis:
                return self.redis.lpop(key)
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
    rpop 从右边弹出数据，并删除数据
    """
    def rpop(self, key):
        self.init()
        try:
            if self.redis:
                return self.redis.rpop(key)
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
    队列长度
    """
    def llen(self, key):
        self.init()
        try:
            if self.redis:
                return self.redis.llen(key)
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
    lrange 获取范围数据
    """
    def lrange(self, key, start, end):
        self.init()
        try:
            if self.redis:
                return self.redis.lrange(key, start, end)
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
     * 查找符合给定模式的key。
     * KEYS *命中数据库中所有key。
     * KEYS h?llo命中hello， hallo and hxllo等。
     * KEYS h*llo命中hllo和heeeeello等。
     * KEYS h[ae]llo命中hello和hallo，但不命中hillo。
     * 特殊符号用"\"隔开
     * 因为这个类加了OPT_PREFIX前缀，所以并不能真的列出redis所有的key，需要的话，要把前缀去掉
    """
    def keys(self, key):
        self.init()
        try:
            if self.redis:
                return self.redis.keys(key)
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
    ttl返回某个key的过期时间
    * 正数：剩余多少秒
    * -1:永不超时
    * -2:key不存在
    """
    def ttl(self, key):
        self.init()
        try:
            if self.redis:
                return self.redis.ttl(key)
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
    exists 检查给定的key是否存在
    * True：存在
    * False：不存在
    """
    def exists(self, key):
        self.init()
        try:
            if self.redis:
                return self.redis.exists(key)
        except Exception as e:
            msg = "Python Fatal error:  Uncaught exception 'RedisException' with message '"+str(e)+"'\n"
            log.error(msg)
        return None
    """
    获取默认配置
    """
    def __get_default_config(self):
        if not inc_config.GLOBALS:
            return {}
        self.rd_configs = inc_config.GLOBALS["config"][0]["redis"]
        return self.rd_configs

