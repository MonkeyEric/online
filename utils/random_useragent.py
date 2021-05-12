# coding:utf-8
# Datetime:2021/5/11 11:14
# __auth__:Eric
# Toolbar: PyCharm
import fake_useragent
import os


def get_header():
    location = os.getcwd() + r'\fake_useragent_0.1.11.json'
    ua = fake_useragent.UserAgent(path=location)
    return ua.random


print get_header()
