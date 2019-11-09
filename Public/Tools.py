#coding=utf-8
import os,sys
import settings
import shutil
import re
from Public import FaceApi
from Public.Logger import logger


def parse_det_result(r_json):
    '''人脸选优参数结果解析'''
    try:
        dic_rlst = r_json
        if not isinstance(dic_rlst,dict):
            return {}
        if not dic_rlst:
            return {}
        if not dic_rlst["faces"]:
            return {}
        face_token = dic_rlst["faces"][0]["face_token"]
        gender = dic_rlst["faces"][0]["attributes"]["gender"]["value"]
        age = dic_rlst["faces"][0]["attributes"]["age"]["value"]
        threshold = dic_rlst["faces"][0]["attributes"]["facequality"]["threshold"]
        value = dic_rlst["faces"][0]["attributes"]["facequality"]["value"]
        surgical_mask_or_respirator = dic_rlst["faces"][0]["attributes"]["mouthstatus"]["surgical_mask_or_respirator"]
        other_occlusion = dic_rlst["faces"][0]["attributes"]["mouthstatus"]["other_occlusion"]
        open = dic_rlst["faces"][0]["attributes"]["mouthstatus"]["open"]
        close = dic_rlst["faces"][0]["attributes"]["mouthstatus"]["close"]
        left_normal_glass_eye_open = dic_rlst["faces"][0]["attributes"]["eyestatus"]["left_eye_status"]["normal_glass_eye_open"]
        left_no_glass_eye_close = dic_rlst["faces"][0]["attributes"]["eyestatus"]["left_eye_status"]["no_glass_eye_close"]
        left_occlusion = dic_rlst["faces"][0]["attributes"]["eyestatus"]["left_eye_status"]["occlusion"]
        left_no_glass_eye_open = dic_rlst["faces"][0]["attributes"]["eyestatus"]["left_eye_status"]["no_glass_eye_open"]
        left_normal_glass_eye_close = dic_rlst["faces"][0]["attributes"]["eyestatus"]["left_eye_status"]["normal_glass_eye_close"]
        left_dark_glasses = dic_rlst["faces"][0]["attributes"]["eyestatus"]["left_eye_status"]["dark_glasses"]
        rigth_normal_glass_eye_open = dic_rlst["faces"][0]["attributes"]["eyestatus"]["right_eye_status"]["normal_glass_eye_open"]
        rigth_no_glass_eye_close = dic_rlst["faces"][0]["attributes"]["eyestatus"]["right_eye_status"]["no_glass_eye_close"]
        rigth_occlusion = dic_rlst["faces"][0]["attributes"]["eyestatus"]["right_eye_status"]["occlusion"]
        rigth_no_glass_eye_open = dic_rlst["faces"][0]["attributes"]["eyestatus"]["right_eye_status"]["no_glass_eye_open"]
        rigth_normal_glass_eye_close = dic_rlst["faces"][0]["attributes"]["eyestatus"]["right_eye_status"]["normal_glass_eye_close"]
        rigth_dark_glasses = dic_rlst["faces"][0]["attributes"]["eyestatus"]["right_eye_status"]["dark_glasses"]
        pitch_angle = dic_rlst["faces"][0]["attributes"]["headpose"]["pitch_angle"]
        yaw_angle = dic_rlst["faces"][0]["attributes"]["headpose"]["yaw_angle"]
        roll_angle = dic_rlst["faces"][0]["attributes"]["headpose"]["roll_angle"]
        blur_blurness_threshold = dic_rlst["faces"][0]["attributes"]["blur"]["blurness"]["threshold"]
        blur_blurness_value = dic_rlst["faces"][0]["attributes"]["blur"]["blurness"]["value"]
        motionblur_threshold = dic_rlst["faces"][0]["attributes"]["blur"]["motionblur"]["threshold"]
        motionblur_value = dic_rlst["faces"][0]["attributes"]["blur"]["motionblur"]["value"]
        gaussianblur_threshold = dic_rlst["faces"][0]["attributes"]["blur"]["gaussianblur"]["threshold"]
        gaussianblur_value = dic_rlst["faces"][0]["attributes"]["blur"]["gaussianblur"]["value"]
        dark_circle = dic_rlst["faces"][0]["attributes"]["skinstatus"]["dark_circle"]
        ethnicity = dic_rlst["faces"][0]["attributes"]["ethnicity"]["value"]
        return {"threshold":threshold,"value":value,"surgical_mask_or_respirator":surgical_mask_or_respirator,
                "other_occlusion":other_occlusion,"open":open,"close":close,"left_occlusion":left_occlusion,
                "left_dark_glasses":left_dark_glasses,"rigth_occlusion":rigth_occlusion,"rigth_dark_glasses":rigth_dark_glasses,
                "blur_blurness_value":blur_blurness_value,"pitch_angle":round(float(pitch_angle),2),"roll_angle":round(float(roll_angle),2),
                "yaw_angle":round(float(yaw_angle),2),"face_token":face_token,"gender":gender,"age":age,
                "dark_circle":dark_circle,"ethnicity":ethnicity,
                }
    except Exception as e:
        print(e)
        return {}

def img_detect_filter(img_path,api_key,api_secret):
    r_json = FaceApi.detect_face(img_path,api_key,api_secret)
    detect_result = parse_det_result(r_json)
    if not detect_result:
        return False
    facetoken = detect_result['face_token']
    gender = detect_result['gender']
    age = detect_result['age']
    threshold = detect_result["threshold"]
    value = detect_result["value"]
    surgical_mask_or_respirator = detect_result["surgical_mask_or_respirator"]
    other_occlusion = detect_result["other_occlusion"]
    opens = detect_result["open"]
    close = detect_result["close"]
    left_occlusion = detect_result["left_occlusion"]
    left_dark_glasses = detect_result["left_dark_glasses"]
    rigth_occlusion = detect_result["rigth_occlusion"]
    rigth_dark_glasses = detect_result["rigth_dark_glasses"]
    blur_blurness_value = detect_result["blur_blurness_value"]
    pitch_angle = detect_result["pitch_angle"]
    roll_angle = detect_result["roll_angle"]
    yaw_angle = detect_result["yaw_angle"]
    dark_circle = detect_result["dark_circle"]
    ethnicity = detect_result["ethnicity"]
    shopname = img_path.split(os.sep)[-5]
    if float(surgical_mask_or_respirator) > settings.surgical_mask_or_respirator or float(other_occlusion) > settings.other_occlusion or float(
        left_occlusion) > settings.left_occlusion or float(left_dark_glasses) > settings.left_dark_glasses or float(
        rigth_occlusion) > settings.rigth_occlusion or float(rigth_dark_glasses) > settings.rigth_dark_glasses or float(
        blur_blurness_value) > settings.blur_blurness_value or abs(float(pitch_angle)) > settings.pitch_angle or abs(float(roll_angle)) > settings.roll_angle or abs(float(yaw_angle)) > settings.yaw_angle:
        return False
    if shopname == "SQ5778A":
        if ethnicity.encode('utf-8') in ["INDIA","WHITE","BLACK"]:
            if float(dark_circle) > 80:
                return False
    return [facetoken,gender,age]


def parse_result_create_set(r_json):
    '''
    {u'faceset_token': u'70b827fba9343de55fb707fbb62b5484', u'time_used': 177, u'face_count': 0, u'face_added': 0, u'request_id': u'1552874113,64eb9e34-9940-4545-8dbf-82388968f993', u'outer_id': u'', u'failure_detail': []}
    '''
    try:
        fs_json = r_json
        if not isinstance(fs_json,dict):
            return {}
        if not fs_json:
            return {}
        fs_token = fs_json["faceset_token"]
        fs_count = fs_json["face_count"]
        return fs_token
    except Exception as e:
        print(e)
        #logging.error(str(e))
        return {}

def parse_result_add_face2set(r_json):
    '''{u'faceset_token': u'70b827fba9343de55fb707fbb62b5484', u'time_used': 614, u'face_count': 1, u'face_added': 1, u'request_id': u'1552874989,36cb1139-9318-409d-b1fe-45ec52d7e28c', u'outer_id': u'', u'failure_detail': []}
    '''
    try:
        add_fs_2_set_json = r_json
        if not isinstance(add_fs_2_set_json,dict):
            return False
        if not add_fs_2_set_json:
            return False
        fs_token = add_fs_2_set_json["faceset_token"]
        fs_added = add_fs_2_set_json["face_added"]
        if fs_token and fs_added:
            return True
    except Exception as e:
        print(e)
        #logging.error(str(e))
        return False

def parse_result_one2N_search(r_json):
    '''{u'time_used': 570, u'thresholds': {u'1e-3': 62.327, u'1e-5': 73.975, u'1e-4': 69.101}, u'results': [{u'confidence': 97.389, u'user_id': u'', u'face_token': u'6c7187f0169cea6e78758c957517af60'}], u'request_id': u'1552875469,490cf66d-6a5f-4b98-8797-5b46f33f10cd'}
    '''
    ch_rst = []
    try:
        one_2_N_search_json = r_json
        if not isinstance(one_2_N_search_json,dict):
            return []
        if not one_2_N_search_json:
            return []
        thresholds = one_2_N_search_json["thresholds"]
        rst_confidence = one_2_N_search_json["results"]
        for rs in rst_confidence:
            confidence = rs["confidence"]
            face_token = rs["face_token"]
            tmp = [confidence,face_token]
            ch_rst.append(tmp)
            print(tmp)
        return ch_rst
    except Exception as e:
        print(e)
        #logging.error(str(e))
        return []


def parse_result_detect(r_json):
    try:
        dic_rlst = r_json
        if not isinstance(dic_rlst, dict):
            return {}
        if not dic_rlst:
            return {}
        face_token = dic_rlst["faces"][0]["face_token"]
        return face_token
    except Exception as e:
        return {}

def convert_create_fs_token_json(json):
    try:
        create_fs_rst = json
        if not isinstance(create_fs_rst,dict):
            return {}
        if not create_fs_rst:
            return {}
        fs_token = create_fs_rst['faceset_token']
        fs_token = fs_token.encode('utf-8')
        return fs_token
    except Exception as e:
        logger.logger.info("create fs token error %s"%str(e))
        return {}

def save_img_facetoken(map_dic):
    file_path = os.path.join(settings.MAP_DIR,'map.txt')
    file = open(file_path,'a+')
    file.write("\n")
    file.write(str(map_dic))
    file.close()
    

def get_imgpath(foldpath):
    try:
        filelist = file_name(foldpath)
        if not filelist:
            return
        img_path = name_chose(filelist)
        return img_path
    except Exception as e:
        print(e)

def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            fpath = os.path.join(root, file)
            fpath = check_fpath(fpath,file)
            if fpath == "continue":
                continue
            L.append(fpath)
    return L

def check_timestamp(s):
    try:
        r1 = r"^[0-9]{10}$"
        r1 = re.compile(r1)
        p = re.search(r1, s)
        return int(p.group(0))
    except Exception as e:
        return "none"

def check_fpath(fpath,file):
    try:
        if not os.path.exists(fpath):
            return "continue"
        file_name_list = file.split("_")
        timestamp = file_name_list[0]
        face = file_name_list[1]
        id_format = file_name_list[2]
        format = id_format.split(".")[1]
        tmesmp = check_timestamp(timestamp)
        if face == "Face" and tmesmp != "none" and format == "jpg":
            return fpath
        else:
            return "continue"
    except Exception as e:
        return "continue"

def name_chose(filelist):
    try:
        for file in filelist:
            name_list = file.split("_")
            if name_list[-1] == "0.jpg":
                return file
            else:
                continue
        return
    except Exception as e:
        print("name_chose   ",e)