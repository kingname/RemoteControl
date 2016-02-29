#-*-coding:utf8-*-
import socket
import util.SocketThread as SocketThread
import threading
import random

class Server:
    BUFFER_SIZE = 2048*100

    def __init__(self, host='', port=5000):
        self.sock = None
        self.host = host
        self.port = port
        self.socketPool = {}
        self.lock = threading.Lock()
        self.connect()
        self.dispatch()


    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.host, self.port))
            # 开启socket监听
            self.sock.listen(5)
        except Exception, e:
            print u'socket 错误: %s' % str(e)
            return None

    def dispatch(self):
        while True:
            if self.sock:
                conn, addr = self.sock.accept()
                print '收到来自 %s的连接' % str(addr[0])
                self.lock.acquire()
                if not addr[0] in self.socketPool:
                    name = addr[0]
                else:
                    name = addr[0] + '-' + str(random.randint(1000, 9999))
                oneSock = SocketThread.SocketThread(conn, name, self.socketPool)
                oneSock.setDaemon(True)
                oneSock.start()
                self.socketPool[name] = conn
                self.lock.release()

if __name__ == '__main__':
    HOST = ''      # 服务器主机地址
    PORT = 5000         # 服务器监听端口

    simple = Server(HOST, PORT)
