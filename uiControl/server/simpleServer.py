#-*-coding:utf8-*-
import socket

class SimpleServer:
    BUFFER_SIZE = 2048*100

    def __init__(self, host='', port=5000):
        self.sock = None
        self.host = host
        self.port = port

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.host, self.port))
            # 开启socket监听
            self.sock.listen(5)
        except Exception, e:
            print 'socket 错误: %s' % str(e)
            return None

    def receive(self):
        if self.sock:
            conn, addr = self.sock.accept()
            print '收到来自 %s的连接' % str(addr)
            while True:
                # 读取数据，数据还没到来阻塞
                data = conn.recv(self.BUFFER_SIZE)
                if len(data):
                    print u'收到来自: %s, 的信息: %s' % (addr[0], data)
                    conn.sendall(u'I have received the data: %s' % data)
                else:
                    print u'socket 连接中断。'
                    break

if __name__ == '__main__':
    HOST = ''      # 服务器主机地址
    PORT = 5000         # 服务器监听端口

    simple = SimpleServer(HOST, PORT)
    simple.connect()
    while True:
        print u'等待连接建立...'
        simple.receive() #进程运行到这里就会阻塞，直到第一次连接主动或者意外断开，才会进入第二次循环。认识到这一点非常重要。
