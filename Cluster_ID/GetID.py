#coding=utf-8
import sys
import os
import datetime
import glob
import pdb
import shutil
from Cluster_ID import Connection
from Cluster_ID.ClusterLog import logger
from Filter.filter import face_filter
from Public.FaceApi import create_faceset
from Public.FaceApi import add_face2set
from Public.FaceApi import one2N_search
from Public.Tools import parse_result_create_set
from Public.Tools import parse_result_one2N_search

def get_license():
    '''
    查询数据库license 查出来key 和 secret
    :return: key secret
    '''
    conn_obj = Connection.Connection()
    license_dic = conn_obj.query_license()
    if not license_dic:
        sys.exit()
    key = license_dic["key"]
    secret = license_dic["secret"]
    return key,secret

def query_faceset_token():
    '''
    根据当天的日期查询出faceset
    :return:返回faceset_token
    '''
    daytime = datetime.datetime.now().strftime("%Y-%m-%d")
    conn = Connection.Connection()
    faceset_token = conn.query_faceset(daytime)
    return faceset_token


def get_faceset_token(key,secret):
    '''
    获取faceset容器biaoshi
    :param key:
    :param secret:
    :return: faceset_token
    '''
    faceset_token = query_faceset_token()
    if not faceset_token:
        create_faceset_json = create_faceset(key,secret)
        faceset_token = parse_result_create_set(create_faceset_json)
    return faceset_token

def get_search_info(faceset_token,facetoken,key,secret):
    '''
    1:N检索 返回置信度最大的facetoken
    :param faceset_token: 容器标识
    :param facetoken: 检索的人脸标识
    :param key: 。。。key
    :param secret: 。。。secret
    :return：非本身图片最大的置信分数
    '''
    search_json = one2N_search(faceset_token,facetoken,key,secret)
    search_lst = parse_result_one2N_search(search_json)
    search_lst = sorted(search_lst,key=lambda x : x[0],reverse=True)
    if len(search_lst) == 1:
    #first 当容器中为空时 执行检索操作只会有本身最相似的结果
        return search_lst[0]
    if len(search_lst) > 1:
        #second 当容器中存在有图片时
        for tmp in search_lst:
            confidence,search_token = tmp
            if search_token == facetoken:
                continue
            return confidence,search_token

def get_today_id(confidende,search_token,facetoken,faceset_token,imgpath):
    '''
    查询数据表给searchtoken 对应的图片赋予id
    :param confidende: 置信分数
    :param search_token: 相似人脸标识
    :param facetoken: 被检索人脸标识
    :param faceset_token: 容器标识
    :return: todayid
    '''
    conn = Connection.Connection()
    max_id = conn.get_all_id()
    if search_token == facetoken:
        todayid = max_id + 1
        conn.save_info_2_db(facetoken, faceset_token, todayid, imgpath)
        return todayid
    else:
        if confidende >= 80.7:
            todayid = conn.get_person_id(search_token)
            if not todayid:
                conn.save_info_2_db(facetoken, faceset_token, todayid, imgpath)
                logger.error("confidence gather than 80.7 bug search token not in database!")
                sys.exit()
            else:
                conn.save_info_2_db(facetoken, faceset_token, todayid, imgpath)
                return todayid
        if confidende < 80.7:
            todayid = max_id + 1
            conn.save_info_2_db(facetoken,faceset_token,todayid,imgpath)
            return todayid

def cluster(imgpath):
    '''
    进行聚类操作
    :param imgpath: 图片路径
    :return: today_id
    '''
    key,secret = get_license()
    filter_result = face_filter(imgpath,key,secret)
    facetoken,gender,age = filter_result
    faceset_token = get_faceset_token(key,secret)
    add_face2set(faceset_token,facetoken,key,secret)
    confidence,search_token = get_search_info(faceset_token,facetoken,key,secret)
    todayid = get_today_id(confidence,search_token,facetoken,faceset_token,imgpath)
    return todayid

if __name__ == "__main__":
    imgpath_lst = glob.glob("/home/zhangyk/workspace/data/img/*/*.jpg")
    for imgpath in imgpath_lst:
        id = cluster(imgpath)
        print(imgpath)
        print(id)
        result_dir = "/home/zhangyk/result/"
        path = os.path.join(result_dir,str(id))
        if not os.path.exists(path):
            os.mkdir(path)
        tar_path = os.path.join(path,os.path.basename(imgpath))
        shutil.copy(imgpath,tar_path)