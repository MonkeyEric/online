# coding:utf-8
import pymongo

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_client["mydb"]

my_col = my_db["ip_proxy"]
if "runoobdb" in my_client.list_database_names():
  print("数据库已存在！")
