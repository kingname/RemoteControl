#-*-coding:utf8-*-

import socket
import json
import threading

class SocketThread(threading.Thread):
    BUFFER_SIZE = 2048*100      # 读取数据大小
    def __init__(self, conn=None, ip=None, socketPool=None):
        threading.Thread.__init__(self)
        print u'生成一个socket， ip地址为: %s' % str(ip)
        self.conn = conn
        self.ip = ip
        self.socketPool = socketPool
        self.lock = threading.Lock()

    def getIp(self):
        return self.ip

    def sendToMaster(self, message):
        self.conn.sendall(self.generateReturn(message))

    def run(self):
        while True:
            # 读取数据，数据还没到来阻塞
            try:
                data = self.conn.recv(self.BUFFER_SIZE)
                if len(data):
                    self.analysisCommand(data)
                else:
                    print u'对方关闭Socket。'
                    self.lock.acquire()
                    if self.ip in self.socketPool:
                        self.socketPool.pop(self.ip)
                    self.lock.release()
                    break
            except Exception, e:
                print u'socket 连接中断。'
                self.lock.acquire()
                if self.ip in self.socketPool:
                    self.socketPool.pop(self.ip)
                self.lock.release()
                break

    def analysisCommand(self, command):
        u'''
        {"from":"master", "to": "xx.xx.xx.xx", "type": "commandInConfig", "command": "xxxx"}
        to的值可能是空，表示在服务器执行，会在是具体IP地址
        {"from":"slave", "info":"xxxx"}

        '''
        try:
            print 'command is %s' % command
            commandDict = json.loads(command)
        except Exception, e:
            print 'command is invaild'
            return ''

        if commandDict:
            commandFrom = commandDict['from']
            if commandFrom == 'master':
                result = self.analysisMasterCommand(commandDict['type'], commandDict['to'], commandDict['command'])
                if result:
                    self.sendToMaster(result)

    def getSlaveList(self):
        self.lock.acquire()
        slaveList = self.socketPool.keys()
        self.lock.release()
        return slaveList

    def generateToSlaveMessage(self, message, commandType):
        return json.dumps({'command': message, 'type': commandType}) + '#finished#'

    def sendToSlave(self, connToSlave, message, commandType):
        print 'in send to slave'
        toSlaveMessage = self.generateToSlaveMessage(message, commandType)
        print u'以下命令将会被发送给被控端: %s' % toSlaveMessage
        try:
            connToSlave.send(toSlaveMessage)
        except Exception, e:
            print u'向被控端发送数据出错：%s' % str(e)

    def generateReturn(self, info):
        returnInfo = {'slaveList': info}
        returnInfo = json.dumps(returnInfo)
        returnInfo = returnInfo + '#finished#'
        print u'以下内容将会返回给控制端: %s' % returnInfo
        return returnInfo

    def analysisMasterCommand(self, commandType, to, command):
        if not to:
            print u'这条命令在服务器上执行， 命令是%s' % command
            if command == 'listSlave':
                return self.getSlaveList()
        print u'这条命令将会在%s上面执行，命令的类型是%s, 命令的内容是:%s' % (to, commandType, command)
        if to not in self.socketPool:
            print u'找不到ip地址为%s的被控端' % to
            return ''
        else:
            self.sendToSlave(self.socketPool[to], command, commandType)
        return ''
