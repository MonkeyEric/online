# coding:utf-8
"""
使用python-dotenv包，来实现mongo数据库的链接，
env的作用：将敏感的数据信息保存起来
"""
import dotenv
import pymongo
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())
config = dotenv.dotenv_values('.env')
# conn = pymongo.MongoClient(config.get('URI'))
# override 参数可以保证即便你更新了env，但是还是最新的，默认是不加载的
conn = pymongo.MongoClient(os.environ.get('URI'), override=True)
if conn:
    print('连接成功！')
