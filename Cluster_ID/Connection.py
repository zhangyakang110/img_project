#coding=utf-8
import sqlite3
import datetime
import os
from Cluster_ID.ClusterLog import logger

class Connection(object):
    def __init__(self):
        self.base_dir = os.path.dirname(__file__)


    def get_conn(self):
        '''
        获取数据库连接
        :return: 返回连接对象
        '''
        db_path = os.path.join(self.base_dir,'cluster.db')
        conn = sqlite3.connect(db_path)
        return conn

    # def save_2_person(self,imgpath,today_id,daytime,faceset,facetoken):
    #     '''
    #     保存参数信息到person数据表
    #     :param imgpath:
    #     :param today_id:
    #     :param daytime:
    #     :param faceset:
    #     :param facetoken:
    #     :return: NONE
    #     '''

    def get_person_id(self,search_facetoken):
        '''
        检索出最相似的人脸id的标识
        :param search_facetoken:检索出最相思的人脸标识
        :return: 返回相似的人脸标识对应的todayid
        '''
        daytime = datetime.datetime.now().strftime("%Y-%m-%d")
        sql = "select todayid from person where facetoken = '%s' and daytime = '%s';"%(search_facetoken,daytime)
        try:
            conn = self.get_conn()
            cu = conn.cursor()
            cu.execute(sql)
            data = cu.fetchall()
            if not data:
                return None
            else:
                tmp = [int(x[0]) for x in data]
                tmp.sort()
                data = tmp[-1]
            return data
        except Exception as e:
            logger.exception(e)
        finally:
            logger.info(sql)
            cu.close()
            conn.close()

    def get_all_id(self):
        '''
        查询出person表中所有的id
        :return: id的最大值
        '''
        daytime = datetime.datetime.now().strftime("%Y-%m-%d")
        sql = "select todayid from person where daytime = '%s';"%(daytime)
        try:
            conn = self.get_conn()
            cu = conn.cursor()
            cu.execute(sql)
            data = cu.fetchall()
            if not data:
                maxid = 0
            else:
                id_lst = [int(x[0]) for x in data]
                id_lst.sort()
                maxid = id_lst[-1]
            return maxid
        except Exception as e:
            logger.exception(e)
        finally:
            logger.info(sql)
            cu.close()
            conn.close()

    def query_license(self):
        '''
        查询key和secret
        :return: 返回key和secret
        '''
        sql = "select key,secret from license;"
        try:
            conn = self.get_conn()
            cu = conn.cursor()
            cu.execute(sql)
            data = cu.fetchall()
            if not data:
                logger.error("license.key-license.secret is none")
                return None
            else:
                key,secret = [data[0][0],data[0][1]]
            return {'key':key,'secret':secret}
        except Exception as e:
            logger.exception(e)
        finally:
            logger.info(sql)
            cu.close()
            conn.close()

    def query_faceset(self,daytime):
        '''
        查询当天的faceset容器标识
        :param daytime:
        :return: facesettoken
        '''
        sql = "select faceset from person where daytime = '%s';"%(daytime)
        try:
            conn = self.get_conn()
            cu = conn.cursor()
            cu.execute(sql)
            data = cu.fetchall()
            if not data:
                return None
            else:
                return data[0][0]
        except Exception as e:
            logger.exception(e)
        finally:
            logger.info(sql)
            cu.close()
            conn.close()

    def save_info_2_db(self,facetoken,faceset,todayid,imgpath):
        '''
        保存检索到的信息到数据库
        :param facetoken: 人脸标识
        :param faceset_token: 容器标识
        :param todayid: 聚类id
        :param imgpath: 图片路径
        :return: None
        '''
        daytime = datetime.datetime.now().strftime("%Y-%m-%d")
        sql = "insert into person (imagepath,todayid,daytime,faceset,facetoken) values('%s','%s','%s','%s','%s');"%(imgpath,todayid,daytime,faceset,facetoken)
        try:
            conn = self.get_conn()
            cu = conn.cursor()
            cu.execute(sql)
            conn.commit()
        except Exception as e:
            logger.exception(e)
            logger.info(sql)
        finally:
            logger.info(sql)
            cu.close()
            conn.close()