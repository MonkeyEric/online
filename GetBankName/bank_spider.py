# coding:utf-8
import time
import requests
import random
from module import col, testcol
from lxml import etree
from multiprocessing import Pool
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def worker(page):
    print '@目前程序正在爬取第______ %s _______页' % page
    url = 'https://www.icvio.cn/bank?region=&bank=&keyword=&per_page=%s' % page
    header = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                            ' (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51',
              'Referer': 'https://www.icvio.cn/'}
    res = requests.get(url, headers=header)

    # 解析数据(使用xpath)
    html = etree.HTML(res.content, etree.HTMLParser())
    for Num in range(2, 12):
        print '@@@@正在爬取第 %s 页， 的第 %s 个div' % (page, Num - 1)
        BankName = html.xpath('/html/body/div[3]/div/div/div[%s]/div[1]/h1/a/text()' % Num)[0]  # 支行名称
        if col.count_documents({'BankName': BankName}) == 0:
            BankCity = html.xpath('/html/body/div[3]/div/div/div[%s]/div[2]/ul/li[2]/a[1]/text()' % Num)[0]  # 支行所在城市
            BankCategory = html.xpath('/html/body/div[3]/div/div/div[%s]/div[2]/ul/li[2]/a[2]/text()' % Num)[
                0]  # 支行所属银行
            BankDetailHref = html.xpath('/html/body/div[3]/div/div/div[%s]/div[2]/a/@href' % Num)[0]  # 支行详情连接网址
            pageNumber = page
            # 存储数据库
            col.insert(
                {'BankName': BankName, 'BankCity': BankCity, 'BankCategory': BankCategory,
                 'BankDetailHref': BankDetailHref,
                 'pageNumber': pageNumber})
    print '@第   %s  页，爬取success' % page
    page += 1

    time.sleep(random.uniform(random.randint(0, 3), random.randint(1, 4)))


def worker_url(data):
    # 将unicode转换为utf-8
    print '^^^^^^^^重新爬取网页    %s' % data['BankName']
    url = 'https://www.icvio.cn/bank?region=&bank=&keyword=%s' % data['BankName']
    header = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                            ' (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51',
              'Referer': 'https://www.icvio.cn/'}
    res = requests.get(url, headers=header)

    # 解析数据(使用xpath)
    html = etree.HTML(res.content, etree.HTMLParser())
    Num = 2
    print '@@@@正在爬取银行    %s      ' % url
    try:
        BankName = html.xpath('/html/body/div[3]/div/div/div[%s]/div[1]/h1/a/text()' % Num)[0]  # 支行名称
    except IndexError:
        testcol.update({'BankName': data['BankName']}, {'$set': {'status': 1}})
        return

    print BankName
    if col.count_documents({'BankName': BankName}) == 0:
        BankCity = html.xpath('/html/body/div[3]/div/div/div[%s]/div[2]/ul/li[2]/a[1]/text()' % Num)[0]  # 支行所在城市
        BankCategory = html.xpath('/html/body/div[3]/div/div/div[%s]/div[2]/ul/li[2]/a[2]/text()' % Num)[
            0]  # 支行所属银行
        BankDetailHref = html.xpath('/html/body/div[3]/div/div/div[%s]/div[2]/a/@href' % Num)[0]  # 支行详情连接网址

        # 存储数据库
        pageNumber = 99999999
        col.insert(
            {'BankName': BankName, 'BankCity': BankCity, 'BankCategory': BankCategory,
             'BankDetailHref': BankDetailHref,
             'pageNumber': pageNumber,
             'CnapsCode': int(data['CnapsCode'])})
        testcol.delete_one({'BankName': BankName})
        print '数据爬取成功，请校验    ', data['CnapsCode']
        time.sleep(random.uniform(random.randint(0, 1), random.randint(1, 2)))
    else:
        print '银行已经存在数据库中…………………………'
        testcol.delete_one({'BankName': data['BankName']})


def main():
    ps = Pool(6)
    for page in range(1473, 14094):
        # ps.apply(worker,args=(i,))     # 同步执行
        ps.apply_async(worker, args=(page,))  # 异步执行
    # 关闭进程池，停止接受其它进程
    ps.close()
    # 阻塞进程
    ps.join()
    print("主进程终止")


def main_url():
    ps = Pool(7)
    data = testcol.find({'status': {'$ne': 1}}, {'_id': 0})
    print '长度为***********    ', data.count()
    for i in data:
        ps.apply_async(worker_url, args=(i,))
    ps.close()
    # 阻塞进程
    ps.join()


if __name__ == '__main__':
    main_url()
