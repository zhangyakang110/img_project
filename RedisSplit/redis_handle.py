# coding=utf-8

import redis
import os
import datetime
import settings
import time
from RedisSplit.RedisLog import logger

FACEKEY = "facesnap_list"

try:
    pool = redis.ConnectionPool(
        host=settings.REDIS_CONFIG["HOST"],
        port=int(settings.REDIS_CONFIG["PORT"]),
        password=settings.REDIS_CONFIG["PASSWORD"],
        db=settings.REDIS_CONFIG['DB'],
        decode_responses=True
    )
    r = redis.Redis(connection_pool=pool)
except Exception as e:
    print e
    logger.error("redis connect error")


def backup(redis_path):
    '''
    备份redis路径
    :param redis_path:rediskey中的图片储存路径
    :return: None
    '''
    path = settings.BACKUP_DIR
    if not os.path.exists(path):
        os.makedirs(path)
    backup_path = os.path.join(path, "backup.txt")
    file = open(backup_path, 'a+')
    file.write("\n")
    file.write(redis_path)


def conver_ip():
    '''
    redis路径切分
    :return: None
    '''
    if not r.exists(FACEKEY):
        print("redis key is null")
        return "redis-none"
    _, redis_path = r.brpop(FACEKEY, timeout=60)
    print(redis_path)
    redis_path = redis_path.encode("utf-8")
    sp_list = redis_path.split(os.sep)
    shopname = sp_list[1]
    r.rpush(shopname, redis_path)
    backup(redis_path)
    print(redis_path)


def main():
    '''
    控制redis切分的时间到达时间后代码结束循环
    :return:
    '''
    while 1:
        try:
            hour = datetime.datetime.now().strftime('%H')
            if int(hour) > 16:
                break
            rst = conver_ip()
            if rst == "redis-none":
                time.sleep(1)
            if not rst:
                continue
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()

