#-*-coding:utf8-*-

import socket
import json
import threading

class SocketHelper(threading.Thread):
    BUFFER_SIZE = 2048*100      # 读取数据大小

    def __init__(self, host=None, port=None, name=None, socketSlavePool=[]):
        threading.Thread.__init__(self, name=name)
        self.host = host
        self.port = port
        self.sock = None
        self.stop = False
        self.name = name
        self.socketSlavePool = socketSlavePool

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.host, self.port))
            # 开启socket监听
            self.sock.listen(5)
        except Exception, e:
            print 'socket error because: %s' % str(e)
            return None

    def receive(self):
        if self.sock:
            conn, addr = self.sock.accept()
            print 'accept a new connect from address: %s' % str(addr)

            command = ''
            while True:
                # 读取数据，数据还没到来阻塞
                data = conn.recv(self.BUFFER_SIZE)
                if len(data):
                    print data
                    command += data
                else:
                    print 'Server Recv finished'
                    print 'the command is: %s' % command
                    return {'conn': conn, 'command': command}

    def analysisCommand(self, rec):
        u'''
        命令将会按照以下格式：
        {'who':{'from': 'master', 'ip': 'xx.xx.xx.xxx'}, 'command': 'yyyyy'}
        {'who':{'from': 'slave', 'ip': 'xx.xx.xx.xxx'}, 'info': 'yyyyy'}
        '''
        conn = rec['conn']
        command = rec['command']
        try:
            commandDict = json.loads(command)
        except Exception, e:
            print 'the command is invaild!'
        whoFrom = commandDict['who']['from']
        if whoFrom == 'master':
            self.doCommand(commandDict['who']['ip'], conn, commandDict['command'])
        elif whoFrom == 'slave':
            self.getSlaveInfo(commandDict['who']['ip'], conn, commandDict['info'])

    def doCommand(self, ip, conn, command):
        print 'ip is: %s' % ip
        print 'command is: %s' % command
        self.socketMasterPool.append({ip: conn})

    def getSlaveInfo(self, ip, conn, info):
        print 'ip is: %s' % ip
        print 'info is: %s' % info
        self.socketSlavePool.append({ip: conn})

    def close(self):
        if self.sock:
            self.sock.close()

    def run(self):
        self.connect()
        print 'connect done!'
        while not self.stop:
            rec = self.receive()
            if rec:
                print 'receive a connect!'
                self.analysisCommand(rec)


    def stop(self):
        self.stop = True
        self.close()
