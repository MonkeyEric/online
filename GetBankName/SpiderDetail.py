# coding:utf-8
import time
import os
import requests
import random
from module import col,col2
from lxml import etree
from multiprocessing import Pool


def worker(url):
    header = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                            ' (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51',
              'Referer': 'https://www.icvio.cn/'}
    res = requests.get(url, headers=header)

    # 解析数据(使用xpath)
    html = etree.HTML(res.content, etree.HTMLParser())
    BankName = html.xpath('//*[@id="post-130344"]/div[3]/p[2]/text()')[0]  # 支行名称
    if col.count_documents({'BankName': BankName}) == 0:
        CnapsCode = html.xpath('/html/body/div[3]/div/div/div[%s]/div[2]/ul/li[2]/a[1]/text()')[0]  # 支行联行号
        BankPhone = html.xpath('//*[@id="post-130344"]/div[3]/p[3]/text()')[
            0]  # 支行联系方式
        BankAddr = html.xpath('//*[@id="post-130344"]/div[3]/p[4]/text()')[0]  # 支行地址
        # 跟新数据库
        col.update(
            {'BankName': BankName}, {'$set': {'CnapsCode': CnapsCode, 'BankPhone': BankPhone,
                                              'BankAddr': BankAddr,
                                              }}
        )
    print 'update %s  success' % BankName
    time.sleep(random.uniform(random.randint(0, 3), random.randint(1, 4)))


def main():
    ps = Pool(3)
    for Page in col.find():
        # ps.apply(worker,args=(i,))     # 同步执行
        ps.apply_async(worker, args=(Page,))  # 异步执行
    # 关闭进程池，停止接受其它进程
    ps.close()
    # 阻塞进程
    ps.join()
    print("主进程终止")


def getAllBank():
    """
    获取全网的银行名字
    :return:
    """
    url = 'http://www.yinhangkahao.com/bank/'
    header = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                            ' (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51',
              'Host': 'www.yinhangkahao.com',
              'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                       'application/signed-exchange;v=b3;q=0.9 ',
              'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
              }
    res = requests.get(url, headers=header)
    html = etree.HTML(res.content, etree.HTMLParser())
    for i in range(1,374):
        listBankName = html.xpath('/html/body/div[1]/div[2]/div[%s]/a/div/div/h5/text()'%i)[0]
        listBankWeb = html.xpath('//html/body/div[1]/div[2]/div[%s]/a/div/div/h6/text()'%i)[0].strip()
        for i in range(len(listBankWeb)):
            col2.insert({'BankName':listBankName,'BankWeb':listBankWeb})
            break


if __name__ == '__main__':
    main()
    # getAllBank()
