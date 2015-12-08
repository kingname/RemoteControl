#-*-coding:utf8-*-

import os
import win32api
from util.mccLog import mccLog

class executor(object):
    def __init__(self, commandDict, openDict):
        self.mccLog = mccLog()
        self.commandDict = commandDict
        self.openDict = openDict

    def execute(self, commandList):
        self.mccLog.mccWriteLog(u'开始处理命令。')
        finishList = []
        for each in commandList:
            innerCommand = each['innerCommand']
            writeCommand = each['writeCommand']
            if not innerCommand:
                self.exeWriteCommand(writeCommand)
            else:
                self.exeInnerCommand(innerCommand)
                self.exeWriteCommand(writeCommand)
            finishList.append(each['_id'])
        return finishList

    def exeInnerCommand(self, innerCommand):
        if innerCommand in self.commandDict:
            self.mccLog.mccWriteLog(u'执行命令')
            try:
                command = self.commandDict[innerCommand]
                os.system(command)
                self.mccLog.mccWriteLog(u'执行命令成功')
            except Exception, e:
                self.mccLog.mccError(u'执行命令失败' + str(e))
        elif innerCommand in self.openDict:
            self.mccLog.mccWriteLog(u'打开文件')
            try:
                openFile = self.openDict[innerCommand]
                win32api.ShellExecute(0, 'open', openFile, '', '', 1)
                self.mccLog.mccWriteLog(u'打开文件成功')
            except Exception, e:
                self.mccLog.mccError(u'打开文件失败：' + str(e))
        else:
            self.mccLog.mccError(u'命令%s不存在！' % innerCommand)

    def exeWriteCommand(self, writeCommand):
            if writeCommand:
                self.sandBox(writeCommand)

    def sandBox(self, code):
        '''
        注意：在网页上面提交的代码请不要出现中文或者中文字符，否则会报错。
        '''
        with open('writeCommand.py', 'w') as f:
            f.write(code)
        os.system('python ' + 'writeCommand.py')
