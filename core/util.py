#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform

if "Linux" in platform.system():
    import fcntl
    

class util:
    """
    写文件，如果文件目录不存在，则递归生成
    """
    def put_file(self, file, content, mode_file="a"):
        self.makdir(file[:file.rfind('\\')])
        f_obj = open(file, mode_file, encoding='utf-8')  # wb 表示打开方式
        if "Linux" in platform.system():
            fcntl.flock(f_obj, fcntl.LOCK_EX)
        f_obj.write(content)
        if "Linux" in platform.system():
            fcntl.flock(f_obj, fcntl.LOCK_UN)
        f_obj.close()

    """
    字典格式化为字符串
    """
    def format_csv(self, fields):
        info = ""
        for key, val in fields:
           info+=key+":"+val.strip()+"|"
        info = info.rstrip("|")
        info+="\n"
        return info

    def makdir(self, dir_path):
        if os.path.exists(dir_path):
            return dir_path
        else:
            os.mkdir(dir_path)
            return dir_path

    # 读文件，返回文件的每一行
    @staticmethod
    def load_file(filename):
        with open(filename, 'r', encoding='UTF-8') as f:
            for i, line in enumerate(f):
                if i == 0:  # 去掉文件第一行的title
                    continue
                yield line.strip('\r\n')
        print('Load % s success!' % filename)

    """
    路径分隔符
    """
    def separator(self):
        if "Windows" in platform.system():
            return "\\"
        elif "Linux" in platform.system():
            return "/"
        return "\\"
