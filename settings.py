#coding=utf-8
import os
import datetime
#oss位置

oss_pfx = "/data/ossfs/"

#店铺列表
shoplist = [
    "MQ2134",
    # "MQ2127",
    # "MQ2110",
    # "SQ2108",
    # "SQ5778A",
    # "SQ2325A",
    # "SQ8501A",
]

#品牌分类
Brand = [
    "MQ2134B",
    # "MQ2127B",
    # "MQ2110B",
    # "SQ2108B",
    # "SQ5778A",
    # "SQ2325A",
    # "SQ8501A",
]

#redis配置信息
REDIS_CONFIG = {
    'HOST':'47.101.18.19',
    'PORT':'6379',
    'PASSWORD':'bgt56yhnPass',
    'DB':'0',
}
BACKUP_KEY = 'test_backup'

#路径相关配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(BASE_DIR,'Backup')



#模型路径相关
MODEL_DIR = os.path.join(BASE_DIR,"MODEL")
deploy = os.path.join(MODEL_DIR,"model.prototxt")
weight = os.path.join(MODEL_DIR,'model.caffemodel')


#路径过滤相关配置
StartTime = 9
FilterCamera = {
    "SQ5778A":{
        "camera_list":[
            "Face_Camera_OUT_04",
            "Face_Camera_OUT_03",
            "Face_Camera_IN_03",],
        "start_time":1030,
        "end_time":1200,},
}

#人脸姿态阈值
surgical_mask_or_respirator = 58
other_occlusion = 60
left_occlusion = 60
rigth_occlusion = 60
left_dark_glasses = 90
rigth_dark_glasses = 90
blur_blurness_value = 35
pitch_angle = 17
roll_angle = 25
yaw_angle = 27

#余弦值
max_cos = 0.5
min_cos = 0.38
cos_count = 5
cos_time = 30

#日期配置
intraday_date = datetime.datetime.now().strftime("%Y-%m-%d")

