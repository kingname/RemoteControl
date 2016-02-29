#-*-coding:utf8-*-

from SocketHelper import SocketHelper

class SocketManager:
    HOST = 'localhost'      # 服务器主机地址
    PORT = 5000         # 服务器监听端口
    BUFFER_SIZE = 2048*100

    def __init__(self):
        self.socketSlavePool = []

    def watch(self):
        socketWatcher = SocketHelper(host=self.HOST, port=self.PORT, name='socketWatcher',
                                     socketSlavePool=self.socketSlavePool)
        socketWatcher.start()

    def heartBeat(self):
        self.socketSlavePool.append({'readFlag': True})
        for each in self.socketSlavePool:
            if each != 'readFlag':
                each.send('heartBeat')
                rec = each.recv(self.BUFFER_SIZE, timeout=5)
                if rec == 'heartBeat':
                    pass

