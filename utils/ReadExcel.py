# coding:utf-8
import json
import uuid

import xlrd
import os
from GetBankName.module import col,testcol
"""
读取excel内容
"""


class readExcel(object):
    def __init__(self, name):
        """获取当前路径"""
        curpath = os.path.dirname(__file__)
        """获取excel文件【与当前脚本在同一级目录下】"""
        self.filename = os.path.join(curpath, name)

        self.excel_handle = xlrd.open_workbook(self.filename)  # 路径不包含中文
        # sheet1 = self.excel_handle.sheet_names()[1]           # 获取第1个sheet的名字,可与获取name函数一起使用
        # sheet = self.excel_handle.sheet_by_name('Sheet1')     # 根据名字获取
        self.sheet = self.excel_handle.sheet_by_index(0)  # 根据索引获取第一个sheet
        # print sheet.name,sheet.nrows,sheet.ncols         # 获取sheet的表格名称、总行数、总列数
        self.row_num = self.sheet.nrows  # 行
        #  col_num = sheet.ncols       # 列

    def readDic(self):
        dic = {}
        arr = []
        row1 = self.sheet.row_values(0)
        # 因为是Unicode编码格式，因此需要转成utf-8
        for i in range(1, self.row_num):
            dic[row1[0].encode('utf-8')] = self.sheet.row_values(i)[0]
            dic[row1[1].encode('utf-8')] = self.sheet.row_values(i)[1].encode('utf-8')
            # dic[row1[2].encode('utf-8')] = self.sheet.row_values(i)[2].encode('utf-8')
            arr.append(dic)
            yield arr


if __name__ == '__main__':
    #     read_excel = readExcel('测试.xlsx'.decode('utf-8').encode('gbk'))
    read_excel = readExcel('yinhangzhihang.xlsx')

    for li in read_excel.readDic():
        # 数据库按照BankName进行查找，如果有，update相应的联行号CnapsCode，没有，则输出停止
        i = li[0]
        if col.count_documents({'BankName': i['BankName']}) == 0:
            i['_id'] = uuid.uuid4()
            testcol.insert(i)
            print '******dont have this bank     ', i['BankName']
        elif col.count_documents({'BankName': i['BankName'],'CnapsCode':int(i['CnapsCode'])})==0:
            col.update({'BankName': i['BankName']},{'$set':{'CnapsCode':int(i['CnapsCode'])}})
            print '######update CnapsCode ', i['BankName']
        else:
            print 'yi jing cun zai ',i['BankName']
    # with open('NoBankName.json','w')as f1:
    #     json.dumps(NoBankName,f1)