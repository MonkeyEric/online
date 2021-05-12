# coding:utf-8
import json
import math
import random
import time
from multiprocessing import Pool

import requests
from multiprocessing.pool import ThreadPool

import time_stamp_change
from modules import HDY_QA

"""
查看互动易公司的网页，爬取公司的文档页面，固定取前10k条数据
"""


def store_data(param):
    i = param[0]
    if HDY_QA.count_documents({'question': i['mainContent']}) == 0 and int(i['contentType']) == 11:
        HDY_QA.insert(
            {
                'company': i['companyShortName'],
                'company_id': param[1],
                'answer': i['attachedContent'],
                'updateDate': time_stamp_change.time_change(int(i['updateDate'])),
                'pubDate': time_stamp_change.time_change(int(i['pubDate'])),
                'trade': i['trade'],
                'stockCode': i['stockCode'],
                'contentType': i['contentType'],
                'question': i['mainContent'],
            }
        )
        print i['companyShortName'], 'save success  '
    elif int(i['contentType']) == 1:
        print '******  %s  公司 the question has not been answered ' % i['companyShortName'].encode('utf-8')
    else:
        print '@@  %s  公司   the question has been saved' % i['companyShortName'].encode('utf-8')


def worker(page_no, qa_data_one):
    stockcode = qa_data_one['_id']
    orgId = qa_data_one['company_id']
    url = 'http://irm.cninfo.com.cn/ircs/company/question'
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
        "stockcode": stockcode,
        "orgId": orgId,
        "pageSize": 1000,
        "pageNum": page_no
    }

    res = requests.post(url=url, data=data, headers=headers)
    if not res.content:
        return
    ResponseData = json.loads(res.content)
    print len(ResponseData['rows'])
    time.sleep(random.uniform(random.randint(1, 2), random.randint(2, 3)))
    # 存储数据，插入没有的数据
    pool = ThreadPool(5)  # 创建一个线程池
    a = [(a, orgId) for a in ResponseData['rows']]
    pool.map(store_data, a)  # 往线程池中填线程
    pool.close()  # 关闭线程池，不再接受线程
    pool.join()


def get_total_page(qa_data_one):
    stockcode = qa_data_one['_id']
    orgId = qa_data_one['company_id']
    url = 'http://irm.cninfo.com.cn/ircs/company/question'
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
        "stockcode": stockcode,
        "orgId": orgId,
        "pageSize": 10,
        "pageNum": 1
    }
    try:
        res = requests.post(url=url, data=data, headers=headers)
        ResponseData = json.loads(res.content)
        # ResponseData['totalPage']
        return ResponseData['total']
    except Exception, e:
        print e
        return


def main():
    QA_data = HDY_QA.aggregate([
        # {"$match": {"company": "友阿股份"}},
        {"$group": {"_id": "$stockCode", "company_id": {'$first': '$company_id'},
                    "company": {"$first": "$company"},
                    "count": {"$sum": 1}}},
        {"$match": {"count": {"$lte":10}}},
        # {"$skip": 266 },
        # {"$limit": 10}
    ])

    for j in QA_data:
        k = get_total_page(j)  # 总共是多少个数据
        print j['company'], '共     %s     个数据' % k
        ps = Pool(1)
        if k:
            for i in range(1, int(math.ceil(k / 1000) + 2)):
                ps.apply_async(worker, args=(i, j))
        ps.close()
        # 阻塞进程
        ps.join()
    print 'the process is over'


if __name__ == '__main__':
    main()
