# coding:utf-8
import time
import requests
import random
from module import chaKaHao
from lxml import etree
from multiprocessing import Pool
import sys
"""
爬取查卡号网的所有银行数据
"""
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def worker(page):
    print '@目前程序正在爬取第______ %s _______页' % page
    url = 'http://www.chakahao.com/lhh/index_%s.html' % page
    header = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51',
              'Host': 'www.chakahao.com',
              "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                        "application/signed-exchange;v=b3;q=0.9",
              "Accept-Encoding": "gzip, deflate",
              "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
              "Connection": "keep-alive"
              }
    res = requests.get(url, headers=header)

    # 解析数据(使用xpath)
    html = etree.HTML(res.content, etree.HTMLParser())
    for Num in range(1, 16):
        # print '@@@@正在爬取第 %s 页， 的第 %s 个div' % (page, Num - 1)
        BankBranch = html.xpath('.//div[@class="table-responsive"]/table/tr[%s]/td[2]/text()' % Num)[0]  # 支行名称
        if chaKaHao.count_documents({'BankBranch': BankBranch}) == 0:
            CnapsCode = html.xpath('/html/body/div/div[2]/div/div/div[1]/div/div[2]/table/tr[%s]/td[3]/a/text()' % Num)[
                0]  # 联行号
            BankBranchHref = \
                html.xpath('/html/body/div/div[2]/div/div/div[1]/div/div[2]/table/tr[%s]/td[3]/a/@href' % Num)[0]
            pageNumber = page
            # 存储数据库
            chaKaHao.insert(
                {'BankBranch': BankBranch,
                 'CnapsCode': CnapsCode,
                 'BankBranchHref': BankBranchHref,
                 'pageNumber': pageNumber})

    print '@第   %s  页，爬取success' % page
    page += 1

    time.sleep(random.uniform(random.randint(0, 2), random.randint(1, 3)))


def main():
    ps = Pool(5)
    for page in range(1, 10233):
        # ps.apply(worker,args=(i,))     # 同步执行
        ps.apply_async(worker, args=(page,))  # 异步执行
    # 关闭进程池，停止接受其它进程
    ps.close()
    # 阻塞进程
    ps.join()
    print("主进程终止")


if __name__ == '__main__':
    main()
