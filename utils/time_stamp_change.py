# coding:utf-8
# 时间戳转北京时间
import time


def time_change(time_stamp):
    time_tuple_1 = time.localtime(time_stamp/1000)
    bj_time = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple_1)
    return bj_time
