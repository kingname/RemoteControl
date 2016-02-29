#-*-coding:utf-8 -*-

from util.configReader import configReader
import SlaveSocket

__Author__ = 'kingname'
__Verson__ = 1.0

class Slave(object):
    CONFIGPATH = '_config.ini'
    KEY_COMMAND = 'Command'
    KEY_OPEN = 'Open'
    KEY_Server = 'Server'
    KEY_Client = 'Client'
    KEY_TIMEOUT = 'timeout'
    KEY_PORT = 'port'

    def __init__(self):
        self.configReader = configReader(self.CONFIGPATH)
        self.timeout = 5
        self.commandDict = {}
        self.openDict = {}
        self.server = ''
        self.port = 5000
        self.initEnv()
        self.run()

    def initEnv(self):
        self.commandDict = self.configReader.getDict(self.KEY_COMMAND)
        self.openDict = self.configReader.getDict(self.KEY_OPEN)
        self.server = self.configReader.getDict(self.KEY_Server)
        print 'Server is: %s' % str(self.server)
        self.timeout = int(self.configReader.readConfig(self.KEY_Client, self.KEY_TIMEOUT))
        print 'init finished'

    def run(self):
        slave = SlaveSocket.SlaveSocket(self.server['host'], int(self.server['port']), self.commandDict, self.openDict, self.timeout)
        slave.setDaemon(True)
        slave.start()
        slave.join()

if __name__=='__main__':
        mcc = Slave()
