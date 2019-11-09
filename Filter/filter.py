#coding=utf-8
import re
import os
import time
import settings
import datetime
from Filter.FilterLog import logger
from Public import Tools

def get_timestamp(imgpath):
    '''使用正则表达式从路径中提取出时间戳'''
    ret = re.search(r'[0-9]{10}',imgpath)
    if not ret:
        return 
    return ret.group()

def get_datetime(imgpath):
    '''获取路径中的时间'''
    ret = re.findall(r'/(\d{8})/',imgpath)
    if not ret:
        return False
    else:
        return ret[0]

def clock_filter(imgpath):
    '''时间过滤  指定时间后开始处理图像'''
    now_timestamp = int(get_timestamp(imgpath))
    struct_time = time.localtime(now_timestamp)
    img_hour = int(time.strftime("%H",struct_time))
    if img_hour < int(settings.StartTime):
        logger.logger.info("%s is %s"%(str(imgpath),str(img_hour)))
        return False
    else:
        return True

def some_shop_filter(imgpath):
    '''某些店铺某些时间点过滤'''
    camera_no = imgpath.split(os.sep)[-3]
    now_timestamp = int((imgpath.split(os.sep)[-1]).split("_")[0])
    struct_time = time.localtime(now_timestamp)
    img_hour = int(time.strftime("%H%M",struct_time))
    shopname = imgpath.split(os.sep)[-5]
    if shopname in settings.FilterCamera and camera_no in settings.FilterCamera[shopname]["camera_list"] and img_hour >= settings.FilterCamera[shopname]["start_time"] and img_hour <= settings.FilterCamera[shopname]["end_time"]:
        return False
    else:
        return True

def face_filter(imgpath,key,secret):
    '''人脸评分接口过滤 不合格返回False  合格返回  age gender facetoken'''
    filter_result = Tools.img_detect_filter(imgpath,key,secret)
    if not filter_result:
        return False
    else:
        return filter_result

def date_filter(imgpath):
    '''日期过滤  非当天日期返回False   当天日期返回True'''
    date_time = get_datetime(imgpath)
    now_datetime = datetime.datetime.now().strftime("%Y%m%d")
    if str(date_time) != str(now_datetime):
        return False
    else:
        return True

def filter(imgpath,key,secret):
    '''过滤模块的调用函数'''
    date_result = date_filter(imgpath)
    clock_result = clock_filter(imgpath)
    some_shop_result = some_shop_filter(imgpath)
    if date_result and clock_filter and some_shop_result:
        filter_result = face_filter(imgpath,key,secret)
        logger.info("%s-%s"%(str(imgpath),str(filter_result)))
        return filter_result
    else:
        logger.info("%s-%s"%(str(imgpath),str("False")))
        return False
