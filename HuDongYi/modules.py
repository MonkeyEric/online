# coding:utf-8
import pymongo
import config

# 连接数据库
client = pymongo.MongoClient(config.MONGO_HOST, config.MONGO_PORT)   # 本地IP，默认端口
db = client['online']  # 进入数据库
HDY_QA = db['HDY_QA']   # 进入集合,互动易问答爬取
col2 = db['HDY_CompanyId']  # 同时保存一个公司与id对应库
