# coding:utf-8
import pymongo
from GetBankName import config

# 连接数据库
client = pymongo.MongoClient(config.MONGO_HOST, config.MONGO_PORT)   # 本地IP，默认端口
db = client['online']  # 进入数据库
col = db['HDY_QA']   # 进入集合,互动易问答爬取