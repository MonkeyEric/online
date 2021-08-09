# coding:utf-8
import random

import config
import selenium
import selenium.webdriver
import time
import json


def write_json(dict_json):
    with open('proxy/ip_proxy_%s.json' % str(time.time()), 'w') as f:
        json.dump(dict_json, f)
        print 'write json success……………………'


def deal_data(content):
    print 'deal data……………………'
    content = content.split('\n')
    lists = []
    for i in content[2:]:
        i = i.split(' ')[:2]
        lists.append({'ip': i[0], 'port': i[1]})

    write_json(lists)


def spider(page):
    # phantomjs.exe  路径需添加系统环境变量    executable_path为环境变量地址
    driver = selenium.webdriver.PhantomJS(executable_path=r"D:\myproject\phantomjs\bin\phantomjs.exe") #打开无界面浏览器
    driver.get("https://www.zdaye.com/FreeIPlist.html?pageid=%s"%page)
    time.sleep(3)
    submitTag = driver.find_element_by_id('ipc')
    ip_text = submitTag.text.encode('utf-8')
    deal_data(ip_text)
    driver.close()


if __name__ == '__main__':
    for i in range(5,20):
        spider(i)