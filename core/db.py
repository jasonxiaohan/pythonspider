#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
db 数据库类文件
Created on 2016年11月23日
@author: DAIXIAOHAN
"""

class db:
    def insert(self, table='', data={}, return_sql=False):
        items_sql=values_sql=""
        for key,value in data.items():
            items_sql+= "`{k}`,".format(k=key)
            values_sql+="\"{v}\",".format(v=value)
        sql = "Insert Ignore Into `"+table+"` ("+items_sql[0:-1]+") Values ("+values_sql[0:-1]+")"
        if return_sql:
            return sql
        else:
            pass
