# coding:utf-8
"""
使用python-dotenv包，来实现mongo数据库的链接，
env的作用：将敏感的数据信息保存起来
"""
import pymongo
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())
conn = False
conn = pymongo.MongoClient(os.environ.get('URI'))
if conn:
    print('连接成功！')
