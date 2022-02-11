#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2018/09/05
# 淘宝秒杀脚本，扫码登录版
import os
from selenium import webdriver
import datetime
import time
from os import path
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
start = datetime.datetime.now()
print('start_time:_____',start)
d = path.dirname(__file__)
abspath = path.abspath(d)
driver = webdriver.Chrome(executable_path="C:\\Users\\16491\\Downloads\\chromedriver_win32\\chromedriver.exe")

driver.maximize_window()


import time, httplib2
# def getBeijinTime():
#     try:
#         conn = httplib2.HTTPConnection("www.beijing-time.org")
#         conn.request("GET", "/time.asp")
#         response = conn.getresponse()
#         print(response.status, response.reason)
#         if response.status == 200:
#             result = response.read()
#             data = result.split("\r\n")
#             year = data[1][len("nyear") + 1: len(data[1]) - 1]
#             month = data[2][len("nmonth") + 1: len(data[2]) - 1]
#             day = data[3][len("nday") + 1: len(data[3]) - 1]
#             # wday = data[4][len("nwday")+1 : len(data[4])-1]
#             hrs = data[5][len("nhrs") + 1: len(data[5]) - 1]
#             minute = data[6][len("nmin") + 1: len(data[6]) - 1]
#             sec = data[7][len("nsec") + 1: len(data[7]) - 1]
#             beijinTimeStr = "%s/%s/%s %s:%s:%s" % (year, month, day, hrs, minute, sec)
#             beijinTime = time.strptime(beijinTimeStr, "%Y/%m/%d %X")
#             return beijinTime
#     except:
#         return None


def login():
    # 打开淘宝登录页，并进行扫码登录
    driver.get("https://www.taobao.com")
    time.sleep(3)
    if driver.find_element_by_link_text("亲，请登录"):
        driver.find_element_by_link_text("亲，请登录").click()

    print("请在30秒内完成扫码")
    time.sleep(30)

    driver.get("https://cart.taobao.com/cart.htm")
    time.sleep(3)
    # 点击购物车里全选按钮
    # if driver.find_element_by_id("J_CheckBox_939775250537"):
    #     driver.find_element_by_id("J_CheckBox_939775250537").click()
    # if driver.find_element_by_id("J_CheckBox_939558169627"):
    #     driver.find_element_by_id("J_CheckBox_939558169627").click()
    if driver.find_element_by_id("J_SelectAll1"):
        driver.find_element_by_id("J_SelectAll1").click()
    now = datetime.datetime.now()
    print('login success:', now.strftime('%Y-%m-%d %H:%M:%S:%f'))


def buy(buytime):
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        print("当前时间" + now)
        # 对比时间，时间到的话就点击结算
        if now >= buytime:
            while True:
                try:
                    # 点击结算按钮
                    if driver.find_element_by_id("J_Go"):
                        driver.find_element_by_id("J_Go").click()
                    driver.find_element_by_link_text('提交订单').click()
                except:
                    time.sleep(0.1)
                # 点击提交订单按钮
                try:
                    if driver.find_element_by_link_text('提交订单'):
                        driver.find_element_by_link_text('提交订单').click()
                        print(f"抢购成功，请尽快付款")
                except:
                    print(f"再次尝试提交订单")
            print(now)
            # time.sleep(0.1)
            # 点击提交订单按钮
            # while True:
            #     try:
            #         if driver.find_element_by_link_text('提交订单'):
            #             driver.find_element_by_link_text('提交订单').click()
            #             print(f"抢购成功，请尽快付款")
            #     except:
            #         print(f"再次尝试提交订单")
            # time.sleep(0.01)


if __name__ == "__main__":
    # times = input("请输入抢购时间：")
    # 时间格式："2018-09-06 11:20:00.000000"

    login()
    print("抢购时间:2022-02-08 16:59:55.000000")
    # buy("2022-02-08 16:59:59.0999999")
    buy("2022-02-09 18:59:59.110209")
