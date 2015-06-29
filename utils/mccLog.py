#-*-coding:utf8-*-
import logging
from datetime import datetime

class mccLog(object):
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename= datetime.now().strftime("%Y%m%d%H%M%S") + '.log',
                filemode='a')
    
    def mccWriteLog(self, logContent):
        logging.info(logContent)

    def mccError(self, errorContent):
        logging.error(errorContent)
