# coding:utf-8
import pymongo
from GetBankName import module

MONGO_HOST = "mongodb://develop:lxjdb2019@117.50.37.209"
MONGO_PORT = 27017

# 连接数据库
client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)  # 本地IP，默认端口

# yunqi数据库，bank 存放bank银行的相关信息
db = client['yunqi']  # 进入数据库
col2 = db['bank_branch']  # 进入集合,互动易问答爬取
# col2.rename('bank_branch')

print col2.find().count()


# data数据库，HDY_QA存放互动易的爬取的数据

def aa():
    db = client['data']  # 进入数据库
    col2 = db['HDY_QA']  # 进入集合,互动易问答爬取
    print col2.find().count()