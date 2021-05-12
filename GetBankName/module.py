# coding:utf-8
import pymongo
import config

# 连接数据库
client = pymongo.MongoClient(config.MONGO_HOST, config.MONGO_PORT)   # 本地IP，默认端口
db = client['online']  # 进入数据库
col = db['GetBankName']   # 进入集合
HDY_QA = db['HDY_QA']

col2 = db['AllBank']      # 中国境内所有银行以及网站（不包含支行）
testcol = db['test']      # 临时数据表
chaKaHao = db['chaKaHao']   # 从查卡号官网爬取的数据
