# coding:utf-8
import requests
import json
import time

url = "http://127.0.0.1:9000/api/channel/auth"
data_ = {
  "profile": {
    "channel_type": "个人渠道",
    "name": "艾瑞克",
    "prefix": "+86",
    "phone": "17302221598",
    "country": "中国",
    "id_card": "130701199310302288",
    "contacts_prefix": "+86"
  },
  "info_imgs": {
    "id_card_front": "https://cdn.51lxj.cn/documents/QpGjcHQLfoAHGERAbB.png",
    "id_card_rever": "https://cdn.51lxj.cn/documents/KgvVqACgeHxe6tCzAL.png",
    "contract_img": "https://cdn.51lxj.cn/documents/hyWLVbEuEYK2SRoTi6.png"
  },
  "step": "2"
}

check_id_card = ['130701199310302288','52030219891209794X','52030219891209794x','52030219891209794Y','32031177070600','3203117707060011','52030219891209794','5203021989120979412','52030219aaaaddd8912','520@#￥%&×302198912','','  ']
check_id_card = ['张三 ','AK张三 ','James Bonde','&*&jzhsan','颤三。。',' **']
for i in check_id_card:
    # data_['profile'].update({'id_card':i})
    data_['profile'].update({'name': i})
    payload = json.dumps(data_)
    headers = {
    'cookie': 'Hm_lvt_469df80d88011b8a7bc8e88a9302500c=1630046886,1631501828; session=f43ac2b3-e0b9-44ce-8536-984712d9191a',
    'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    print('开始字段测试————————')
    print(data_['profile']['name'])
    print(json.loads(response.content))

    time.sleep(3)
