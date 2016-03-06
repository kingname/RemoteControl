#-*-coding:utf8-*-
import socket
import threading
import time
import json
from util.excutor import executor

class SlaveSocket(threading.Thread):
    BUFFER_SIZE = 2048*100

    def __init__(self, host='', port=5000, commandDict=None, openDict=None, timeout=5):
        threading.Thread.__init__(self)
        self.connected = False
        self.sock = None
        self.host = host
        self.port = port
        self.stop = False
        self.timeout = timeout
        self.executor = executor(commandDict, openDict)

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
            while not self.stop:
                if not self.connected:
                    print u'开始连接...'
                    if self.connect():
                        print u'连接成功'
                else:
                    try:
                        data = self.sock.recv(self.BUFFER_SIZE)
                        if len(data):
                            self.analysisCommand(data)
                        else:
                            print u'socket 连接中断。'
                            break
                    except Exception, e:
                        print 'socket error, because: %s ' % str(e)
                        self.connected = False
                        continue

    def analysisCommand(self, data):
        u'''
        {"command":"xxx", "type":"commandInConfig"}
        '''
        print u'接受到的命令是: %s' % data
        if data:
            try:
                commandDict = json.loads(data[:-10])
            except Exception, e:
                print u'命令格式不对。'
                return ''
            print str(commandDict)
            commandType = commandDict['type']
            command = commandDict['command']
            if command == 'runaway':
                self.stop = True
                self.sock.close()
            else:
                self.executor.execute(commandType, command)


