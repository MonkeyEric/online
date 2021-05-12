# coding:utf-8
import json
import random
import time
from multiprocessing import Pool

import requests

import time_stamp_change
from modules import HDY_QA


def worker(page_no):
    time.sleep(random.uniform(random.randint(1, 2), random.randint(2, 3)))
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
        "page_no": page_no,
        "pageSize": "100",
        "searchTypes": "11"
    }
    res = requests.post(url=url, data=data, headers=headers)
    ResponseData = json.loads(res.content)

    # 存储数据，插入没有的数据
    for i in ResponseData['results']:
        if HDY_QA.count_documents({'question': i['mainContent'], 'company_id': i['secid']}) == 0:
            HDY_QA.insert(
                {
                    'company': i['companyShortName'],
                    'company_id': i['secid'],
                    'answer': i['attachedContent'],
                    'updateDate': time_stamp_change.time_change(int(i['updateDate'])),
                    'pubDate': time_stamp_change.time_change(int(i['pubDate'])),
                    'trade': i['trade'],
                    'stockCode': i['stockCode'],
                    'contentType': i['contentType'],
                    'question': i['mainContent']
                }
            )
            print i['companyShortName'], 'save success'
        else:
            print 'the question has been saved'


def main():
    ps = Pool(2)
    for i in range(1, 2):
        ps.apply_async(worker, args=(i,))
        time.sleep(60)
    ps.close()
    # 阻塞进程
    ps.join()


if __name__ == '__main__':
    main()
#  隔1隔小时
