# coding=utf-8

"""
File Name: post_rst.py
Author: Zhangyk
Created Time: 2018-10-17
"""

import json
import sys
import requests
import datetime
from post_rst import MapLog

reload(sys)
sys.setdefaultencoding('utf-8')

def post_data(data_dic):
    """
    :param data_dic:字典类型{} 数据格式：
        {'dealerCode': 'SQ2108', 'reserved': '4Simage/SQ2108/20181008/Face_Camera_IN_01/', 'imageFixNumber': 836, 'timestamp': 1538960108, 'sex': 'M', 'imageValid': 'Y', 'oldFlag': 'Y', 'custId': '9', 'ageGroup': '26-36'}
    :return: 发送数据后的返回状态结果
        1:发送成功之后返回值为 1     发送后的结果示例--{"errorCode": 0,"result": {"class": "com.saicmotor.cep.pss.model.Result","obj": "保存成功！","success": 1}}
        2:发送失败之后返回值为 api文档中的失败状态码  60101001---60101008  调用 url 不符合规范...
        3：假如 传入的参数不是字典类型  返回值为"error"
        4:否则出现其他情况则为发送失败,并且返回值为    none
    """
    try:
        if not isinstance(data_dic, dict):
            return "error"
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        #请求头信息
        headers = {"Content-Type": "application/json",
                   "appKey": "key1",
                   "timestamp": now,
                   "signature": "471C2389457329486JKHFI"}
        rest_api_url = "https://mdapp-pv.saicmotor.com/services/IntelligentReceptionApi/intelligentReception" 
        data_dic = {'intelligentReceptionList': [data_dic]}
        data_dic = json.dumps(data_dic)
        print data_dic
        result = requests.post(rest_api_url, data=data_dic, headers=headers).text
        #result = {"errorCode":0,"result":{"class":"com.saic.intelligent.model.Result","msg":"[test XXXXXXXXXXXX]","success":0}}
        print result
        result = json.loads(result)
        MapLog.logger.info(result," ",str(data_dic))
    except Exception as e:
        MapLog.logger.exception(e)


if __name__ == "__main__":
    picname = "1538122785_face_1779"
    post_data(picname)
