# coding:utf-8
import requests
import json
from modules import col
from multiprocessing import Pool
from utils import TimestampChange


def worker(pageNo):
    url = 'http://irm.cninfo.com.cn/ircs/index/search'
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "irm.cninfo.com.cn",
        "Origin": "http://irm.cninfo.com.cn",
        "Referer": "http://irm.cninfo.com.cn/ircs/index",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51 X-Requested-With: XMLHttpRequest "
    }
    data = {
        "pageNo": pageNo,
        "pageSize": "10",
        "searchTypes": "11"
    }
    res = requests.post(url=url, data=data, headers=headers)
    data = json.loads(res.content)

    # 存储数据，插入没有的数据

    print 1111
    for i in data['results']:
        if col.count_documents({'mainContent': i['mainContent']}) == 0:
            col.insert(
                {
                    'companyShortName': i['companyShortName'],
                    'attachedContent': i['attachedContent'],
                    'updateDate': TimestampChange.TimeChange(i['updateDate']),
                    'pubDate': TimestampChange.TimeChange(i['pubDate']),
                    'trade': i['trade'],
                    'stockCode': i['stockCode'],
                    'contentType': i['contentType'],
                    'mainContent': i['mainContent']
                }
            )


def main():
    ps = Pool(5)
    for i in range(1, 100):
        ps.apply_async(worker, args=(i,))
    ps.close()
    # 阻塞进程
    ps.join()


if __name__ == '__main__':
    main()
