# coding:utf-8
# 时间戳转北京时间
import time


def TimeChange(Date):
    time_tuple_1 = time.localtime(Date/1000)
    bj_time = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple_1)
    print("北京时间：", bj_time)
    return bj_time
