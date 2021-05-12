# coding:utf-8
import pymongo
from GetBankName import module

MONGO_HOST = "mongodb://develop:lxjdb2019@117.50.37.209"
MONGO_PORT = 27017

# 连接数据库
client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)  # 本地IP，默认端口
db = client['data']  # 进入数据库
col2 = db['HDY_QA']  # 进入集合,互动易问答爬取

HDY_QA = module.HDY_QA.aggregate([{"$project": {'_id': 0}},

                                  # {"$limit": 10}
                                  ],
                                 allowDiskUse=True)
for j in list(HDY_QA):
    if col2.count_documents({"question": j["question"]}) == 0:
        col2.insert(j)
        print 'insert success'
    else:
        print '$$$$$ the database has been saved'
