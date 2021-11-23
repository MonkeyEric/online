# coding:utf-8
import re

# -*- coding: utf-8 -*-
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def checkIdcard(idcard):
    Errors = ['ok', '身份证号码位数不对!', '身份证号码出生日期超出范围或含有非法字符!', '身份证号码校验错误!', '身份证地区非法!', '身份证号码不能为空']
    area = {"11": "北京", "12": "天津", "13": "河北", "14": "山西", "15": "内蒙古", "21": "辽宁", "22": "吉林", "23": "黑龙江",
            "31": "上海",
            "32": "江苏", "33": "浙江", "34": "安徽", "35": "福建", "36": "江西", "37": "山东", "41": "河南", "42": "湖北", "43": "湖南",
            "44": "广东", "45": "广西", "46": "海南", "50": "重庆", "51": "四川", "52": "贵州", "53": "云南", "54": "西藏", "61": "陕西",
            "62": "甘肃", "63": "青海", "64": "宁夏", "65": "新疆", "71": "台湾", "81": "香港", "82": "澳门", "91": "国外"}
    idcard = str(idcard)
    if idcard[-1] == 'x':
        return {'code': '100000', 'msg': '身份证号码字母需大写'}
    idcard = idcard.strip()
    idcard_list = list(idcard)

    # 地区校验
    key = idcard[0: 2]  # TODO： cc  地区中的键是否存在
    if not idcard:
        return {'code': '100111', 'msg': Errors[5]}
    if key in area.keys():
        if not area[(idcard)[0:2]]:
            return {'code': '100111', 'msg': Errors[4]}
    else:
        return {'code': '100111', 'msg': Errors[4]}
    # 15位身份号码检测

    if len(idcard) == 15:
        if ((int(idcard[6:8]) + 1900) % 4 == 0 or (
                (int(idcard[6:8]) + 1900) % 100 == 0 and (int(idcard[6:8]) + 1900) % 4 == 0)):
            ereg = re.compile(
                '[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}$')  # //测试出生日期的合法性
        else:
            ereg = re.compile(
                '[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}$')  # //测试出生日期的合法性
        if re.match(ereg, idcard):
            return {'code': '100000', 'msg': Errors[0]}
        else:
            return {'code': '100111', 'msg': Errors[2]}
    # 18位身份号码检测
    elif len(idcard) == 18:
        # 出生日期的合法性检查
        # 闰年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))
        # 平年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))
        try:
            if int(idcard[6:10]) % 4 == 0 or (int(idcard[6:10]) % 100 == 0 and int(idcard[6:10]) % 4 == 0):
                ereg = re.compile(
                    '[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$')  # //闰年出生日期的合法性正则表达式
            else:
                ereg = re.compile(
                    '[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$')  # //平年出生日期的合法性正则表达式
        except:
            return {'code': '100111', 'msg': Errors[2]}
        # //测试出生日期的合法性
        if re.match(ereg, idcard):
            # //计算校验位
            S = (int(idcard_list[0]) + int(idcard_list[10])) * 7 + (int(idcard_list[1]) + int(idcard_list[11])) * 9 + (
                    int(
                        idcard_list[2]) + int(idcard_list[12])) * 10 + (
                        int(idcard_list[3]) + int(idcard_list[13])) * 5 + (int(
                idcard_list[4]) + int(idcard_list[14])) * 8 + (int(idcard_list[5]) + int(idcard_list[15])) * 4 + (int(
                idcard_list[6]) + int(idcard_list[16])) * 2 + int(idcard_list[7]) * 1 + int(idcard_list[8]) * 6 + int(
                idcard_list[9]) * 3
            Y = S % 11
            M = "F"
            JYM = "10X98765432"
            M = JYM[Y]  # 判断校验位
            if M == idcard_list[17]:  # 检测ID的校验位
                return {'code': '100000', 'msg': Errors[0]}
            else:
                return {'code': '100111', 'msg': Errors[3]}
        else:
            return {'code': '100111', 'msg': Errors[2]}
    else:
        return {'code': '100111', 'msg': Errors[1]}


def re_tools(data):
    # 手机号
    if data.get('phone'):
        try:
            if data.get('prefix') == "+86":
                if re.match("^1(3|4|5|6|7|8|9)\d{9}$|^852\d{8}$", data.get('phone')) is None:
                    return {"code": "100101", "msg": u"手机格式错误，请重新填写！"}
            else:
                if re.match("\d+", data.get('phone')) is None:
                    return {"code": "100101", "msg": u"手机格式错误，请重新填写！"}
        except:
            return {"code": "100111", "msg": u"手机格式验证，缺少参数！"}

    if data.get('name'):
        try:
            # 个人姓名:可输入：汉字 字母 空格；
            if data['channel_type'] == '个人渠道':
                if re.match(u'^[\u4E00-\u9FA5A-Za-z_\s]+$', data.get('name')) is None:
                    return {"code": "100101", "msg": u"个人渠道的姓名格式错误，请重新填写"}
            # 机构姓名：格式支持：汉字、字母、空格、括号
            elif data['channel_type'] == '机构渠道':
                if re.match('^[\u4E00-\u9FA5A-Za-z_\s\(\)\（\）]+$', data.get('name')) is None:
                    return {"code": "100101", "msg": u"机构渠道的姓名格式错误，请重新填写"}
        except:
            return {"code": "100111", "msg": u"姓名验证，缺少参数"}

    # 身份证号：  若国家为中国，需正则校验；若国家非中国，支持格式：数字、字母、中英文括号 横线；
    if data.get('id_card'):
        if data.get('country') == '中国':
            res = checkIdcard(data.get('id_card'))
            if res.get('code') != '100000':
                return res
        else:
            if re.match('^[\da-zA-Z\(\)\-\（\）]+$', data.get('id_card')) is None:
                return {"code": "100101", "msg": u"身份证格式错误，请重新填写！(国家:非中国)"}

    if data.get('registration_certificate'):
        # 商业登记号： 格式支持：汉字、数字、字母、中英文横线、中英文括号
        if re.match('^[\u4E00-\u9FA5\dA-Za-z\-\——\(\)\（\）]+$', data.get('registration_certificate')) is None:
            return {"code": "100101", "msg": u"商业登记号格式错误，请重新填写！"}

    if data.get('email'):
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$",
                    data['email']) is None:
            return {"code": "100001", "msg": u"邮箱格式错误，请重新填写！"}


if __name__ == "__main__":

    # print(re_tools({'id_card':'中国后i吧qowiueqon-（）1231451234dajsiq','country':'中国'}))
    print(re_tools({'name':'AK张三'.decode('utf8'),'channel_type':'个人渠道'}))
    person_name = ['Ak张三', '张三Ak', ' ak 颤三', 'ask asd qwd qvc']
    org_name = ['Ak张三', '张三Ak', ' ak 颤三', 'ask asd qwd qvc', '(AK中国三', ')AK权威的 qqw', '（）读取啊是第几ak as qwd', '张三AK()',
                '张三AK（ ）']
    for i in person_name:
        print re_tools({'name': i.decode('utf-8'), 'channel_type': '个人渠道'})
    # print(re_tools({'phone':'1233512a','prefix':'+86'}))
    # print(re_tools({'registration_certificate':'——北京分公司2-103242asdqwd'}))