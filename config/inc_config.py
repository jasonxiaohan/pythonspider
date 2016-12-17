#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
mysql、redis配置信息
"""
GLOBALS = {
    "config": [
        {
            "db":
                {
                    "host": "127.0.0.1",
                    "port": 3306,
                    "user": "root",
                    "pass": "root",
                    "name": "demo"
                },
            "redis":
                {
                    "host": "127.0.0.1",
                    "port": 6379,
                    "pass": "",
                    "prefix": "pythonspider",
                    "db": 0,
                    "timeout": 30
                }
         }
    ]
}

