#-*-coding:utf8-*-
import socket
import threading
import time
import json

class MasterSocket(threading.Thread):
    BUFFER_SIZE = 2048*100

    def __init__(self, host='', port=5000, command='', serverList=None, commandType='', to='', timeout=5):
        threading.Thread.__init__(self)
        self.connected = False
        self.sock = None
        self.host = host
        self.port = port
        self.command = command
        self.timeout = timeout
        if serverList is not None:
            self.serverList = serverList

        if to:
            self.to = to
        else:
            self.to = ''
        if commandType:
            self.commandType = commandType
        else:
            self.commandType = ''

    def connect(self):
        startTime = time.time()
        timeDelta = 0
        while timeDelta <= self.timeout:
            try:
            # 创建客户端套接字
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # 连接到服务器
                self.sock.connect((self.host, self.port))
                self.connected = True
                return True
            except Exception, _:
                time.sleep(1)
                timeDelta = int(time.time() - startTime)
        if timeDelta > self.timeout:
            print u'连接超时'
            return False

    def run(self):
        print u'开始连接...'
        if self.connect():
            print u'连接成功'
            try:
                self.send(self.command)
            except Exception, e:
                print 'socket error, because: %s ' % str(e)

    def generateJson(self, fromWhere, command, to='', commandType=''):
        commandDict = {'from': fromWhere, 'to': to, 'command': command, 'type': commandType}
        return json.dumps(commandDict)

    def send(self, command):
        print u'往服务器发送数据: %s' % command
        receiveData = ''
        try:
            # 发起数据给服务器
            self.sock.sendall(self.generateJson('master', command, to=self.to, commandType=self.commandType))

            while '#finished#' not in receiveData:
                # 接收服务器返回的数据
                data = self.sock.recv(self.BUFFER_SIZE)
                receiveData += data
            print u'收到服务器返回： %s' % receiveData
            self.analysisResult(receiveData)

        except socket.errno, e:
            print 'Socket error: %s' % str(e)
        except Exception, e:
            print 'Other exception: %s' % e
        finally:
            print u'关闭socket'
            self.sock.close()

    def analysisResult(self, result):
        print u'开始分析返回信息： %s' % result
        if result:
            try:
                resultDict = json.loads(result[:-10])
            except Exception, e:
                print u'返回信息有误'
                return ''
            if 'slaveList' in resultDict:
                self.serverList += resultDict['slaveList']
                print u'被控端列表: %s' % str(self.serverList)
                # self.sock.close()


