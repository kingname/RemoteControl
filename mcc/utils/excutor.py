#-*-coding:utf8-*-

import os
import win32api
import logging
from utils.mailHelper import mailHelper

class executor(object):
    def __init__(self, commandDict, openDict):
        self.mccLog = logging.getLogger('mcc')
        self.commandDict = commandDict
        self.openDict = openDict

    def execute(self, exe, mailHelper):
        self.mailHelper = mailHelper
        subject = exe['subject']
        self.mccLog.info('开始处理命令。')
        self.mailHelper.sendMail('pass','Slave')
        if subject in self.commandDict:
            self.mccLog.info('执行命令')
            try:
                command = self.commandDict[subject]
                os.system(command)
                self.mailHelper.sendMail('Success','Boss')
                self.mccLog.info('执行命令成功')
            except Exception as e:
                self.mccLog.error('执行命令失败' + str(e))
                self.mailHelper.sendMail('error', 'Boss', e)
        elif subject in self.openDict:
            self.mccLog.info('打开文件')
            try:
                openFile = self.openDict[subject]
                win32api.ShellExecute(0, 'open', openFile, '', '', 1)
                self.mailHelper.sendMail('Success', 'Boss')
                self.mccLog.info('打开文件成功')
            except Exception as e:
                self.mccLog.error('打开文件失败：' + str(e))
                self.mailHelper.sendMail('error', 'Boss', e)
        elif subject[:7].lower() == 'sandbox':
                self.sandBox(subject[8:])
        else:
            self.mailHelper.sendMail('error', 'boss', 'no such command')

    def sandBox(self, code):
        """sandbox:test.py$n$import win32api$c$if 1 + 1 == 2:$c$$$$$win32api.MessageBox(0, 'sandbox', 'this is sandbox')"""

        name = code.split('$n$')[0]
        code = code.split('$n$')[1]
        codestr = '\n'.join(code.split('$c$'))
        codestr = codestr.replace('$', ' ')
        with open(name, 'w') as f:
            f.write(codestr)
        os.system('python ' + name)
