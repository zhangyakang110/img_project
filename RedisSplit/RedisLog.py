#coding=utf-8

import os
import logging
import settings
import datetime

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'log')
if not os.path.exists(log_file_path):
    os.makedirs(log_file_path)
stamp_time = datetime.datetime.now().strftime("%Y%m%d")
log_name = stamp_time + ".log"
log_name_path = os.path.join(log_file_path,log_name)

logger = logging.getLogger()
handler = logging.FileHandler(log_name_path)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
