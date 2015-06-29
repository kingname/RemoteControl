#-*-coding:utf-8 -*-

import time
import sys
from utils.mailHelper import mailHelper
from utils.excutor import executor
from utils.configReader import configReader

__Author__ = 'kingname'
__Verson__ = 0.5

reload(sys)
sys.setdefaultencoding('utf-8')

class MCC(object):
    CONFIGPATH = '_config.ini'
    KEY_COMMAND = 'Command'
    KEY_OPEN = 'Open'

    def __init__(self):
        # self.mccLog = mccLog()
        self.mailHelper = mailHelper()
        self.configReader = configReader(self.CONFIGPATH)
        commandDict = self.configReader.getDict(self.KEY_COMMAND)
        openDict = self.configReader.getDict(self.KEY_OPEN)
        self.excutor = executor(commandDict, openDict)
        self.run()

    def run(self):
        mailBody = self.mailHelper.acceptMail()
        if mailBody:
            exe = self.mailHelper.analysisMail(mailBody)
            if exe:
                self.excutor.execute(exe)

if __name__=='__main__':
        mcc = MCC()
        time.sleep(5)


