# coding=utf-8
import requests
import glob
import os
import json
import shutil
import base64
import pdb
import time



def detect_face(img_file_path,api_key,api_secret):
    pay_load = {
        'api_key': api_key,
        'api_secret': api_secret,
        'return_attributes': 'facequality,headpose,blur,eyestatus,mouthstatus,age,gender,skinstatus,ethnicity'
    }
    image_file = {'image_file': open(img_file_path, 'rb')}
    r = requests.post("https://api-cn.faceplusplus.com/facepp/v3/detect", data=pay_load, files=image_file)
    # print("+++++++++++++++++++++++++++++++++++detect_face++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    # print(img_file_path)
    # print(r.status_code)
    # print(r.text)
    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    r_json = json.loads(r.text)
    if r.status_code == 200:
        return r_json
    elif r_json['error_message'] == "CONCURRENCY_LIMIT_EXCEEDED":
        time.sleep(1)
        return detect_face(img_file_path,api_key,api_secret)
    elif r.status_code != 200:
        time.sleep(1)
        return detect_face(img_file_path,api_key,api_secret)


def create_faceset(api_key,api_secret):
    '''
    创建人脸库
    url：https://api-cn.faceplusplus.com/facepp/v3/faceset/create
    调用方式:POST
    :return:faceset_token
    '''
    pay_load = {
        'api_key': api_key,
        'api_secret': api_secret,
    }
    create_faceset_url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/create"
    r = requests.post(create_faceset_url, data=pay_load)
    # print("+++++++++++++++++++++++++++++++++++create face++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    # print(r)
    # print(r.status_code)
    # print(r.text)
    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    r_json = json.loads(r.text)
    if r.status_code == 200:
        return r_json
    elif r_json['error_message'] == "CONCURRENCY_LIMIT_EXCEEDED":
        time.sleep(1)
        return create_faceset(api_key,api_secret)
    elif r.status_code != 200:
        time.sleep(1)
        return create_faceset(api_key,api_secret)
        
def del_faceset(faceset_token,api_key,api_secret):
    '''
    删除人脸库
    url：https://api-cn.faceplusplus.com/facepp/v3/faceset/delete
    调用方式:POST
    '''
    pay_load = {
        'api_key': api_key,
        'api_secret': api_secret,
        'faceset_token': faceset_token,
        'check_empty': 0,
    }
    del_faceset_url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/delete"
    r = requests.post(del_faceset_url, data=pay_load)
    # print("+++++++++++++++++++++++++++++++++++delete faceset token++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    # print(faceset_token)
    # print(r)
    # print(r.status_code)
    # print(r.text)
    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    r_json = json.loads(r.text)
    if r.status_code == 200:
        return r_json
    elif r_json['error_message'] == "CONCURRENCY_LIMIT_EXCEEDED":
        time.sleep(1)
        return del_faceset(faceset_token,api_key,api_secret)
    elif r.status_code != 200:
        time.sleep(1)
        return del_faceset(faceset_token,api_key,api_secret)

def add_face2set(faceset_token, face_tokens,api_key,api_secret):
    '''
    向人脸库添加人脸
    url：https://api-cn.faceplusplus.com/facepp/v3/faceset/addface
    调用方式:POST
    '''
    pay_load = {
        'api_key': api_key,
        'api_secret': api_secret,
        'faceset_token': faceset_token,
        'face_tokens': face_tokens,
    }
    add_face2set_url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/addface"
    r = requests.post(add_face2set_url, data=pay_load)
    # print("+++++++++++++++++++++++++++++++++++add face to set++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    # print(face_tokens)
    # print(r)
    # print(r.status_code)
    # print(r.text)
    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    r_json = json.loads(r.text)
    if r.status_code == 200:
        return r_json
    elif r_json['error_message'] == "CONCURRENCY_LIMIT_EXCEEDED":
        time.sleep(1)
        return add_face2set(faceset_token, face_tokens,api_key,api_secret)
    elif r.status_code != 200:
        time.sleep(1)
        return add_face2set(faceset_token, face_tokens,api_key,api_secret)

def one2N_search(faceset_token, face_token,api_key,api_secret):
    '''
    向人脸库添加人脸
    url：https://api-cn.faceplusplus.com/facepp/v3/search
    调用方式:POST
    '''
    pay_load = {
        'api_key': api_key,
        'api_secret': api_secret,
        'faceset_token': faceset_token,
        'face_token': face_token,
        'return_result_count': 5
    }
    one2N_search_url = "https://api-cn.faceplusplus.com/facepp/v3/search"
    
    r = requests.post(one2N_search_url, data=pay_load)
    # print("+++++++++++++++++++++++++++++++++++one2N_search++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    # print(face_token)
    # print(r)
    # print(r.status_code)
    # print(r.text)
    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    r_json = json.loads(r.text)
    if r.status_code == 200:
        return r_json
    elif r_json['error_message'] == "CONCURRENCY_LIMIT_EXCEEDED":
        time.sleep(1)
        return one2N_search(faceset_token, face_token,api_key,api_secret)
    elif r.status_code != 200:
        time.sleep(1)
        return one2N_search(faceset_token, face_token,api_key,api_secret)

def remove_face(faceset_token, face_tokens,api_key,api_secret):
    '''
    从faceset中删除人脸
    url：https://api-cn.faceplusplus.com/facepp/v3/faceset/removeface
    调用方式:POST
    '''
    pay_load = {
        'api_key': api_key,
        'api_secret': api_secret,
        'faceset_token': faceset_token,
        'face_tokens': face_tokens,
    }
    remove_face_url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/removeface"
    r = requests.post(remove_face_url, data=pay_load)
    # print("+++++++++++++++++++++++++++++++++++remove_face++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    # print(face_tokens)
    # print(r)
    # print(r.status_code)
    # print(r.text)
    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    r_json = json.loads(r.text)
    if r.status_code == 200:
        return r_json
    elif r_json['error_message'] == "CONCURRENCY_LIMIT_EXCEEDED":
        time.sleep(1)
        return remove_face(faceset_token, face_tokens,api_key,api_secret)
    elif r.status_code != 200:
        time.sleep(1)
        return remove_face(faceset_token, face_tokens,api_key,api_secret)


