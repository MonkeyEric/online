# coding:utf-8
# Datatime:2021/5/12 12:09
# __auth__:Eric
# Toolby: PyCharm
import logging


def loger():
    # 1、创建一个logger
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)

    # 2、创建一个handler，用于写入日志文件
    fh = logging.FileHandler('hdy_spider.log')
    fh.setLevel(logging.DEBUG)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # 3、定义handler的输出格式（formatter）
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 4、给handler添加formatter
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 5、给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)

