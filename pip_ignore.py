# coding=utf-8
"""
脚本功能：
1、pip安装所有文件，忽视错误，不会出现终止
2、自动重新安装未安装的文件（此次不会要求版本的问题）
"""

import pip
from subprocess import call

filename = 'requirements.txt'
with open(filename)as f:
    for dist in f.readlines():
        print dist

        call("pip install --upgrade " + dist.replace('/r','').replace('/n','').replace('/t',''), shell=True)


