#-*-coding:utf8-*-

import wx
from MasterSocket import MasterSocket
import threading

# SERVER = '128.199.151.202'
SERVER = '192.168.2.100'
PORT = 5000

'''基于Sizer的控件相对布局'''
class Slave(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1, title=u'极客学院', size=(600, 600))
        self.panel = wx.Panel(self, -1)
        self.lock = threading.Lock()
        self.Centre()

        #定义我们需要的各个控件

        commandStatic = wx.StaticText(self.panel, -1, u'输命令:')
        writePyStatic = wx.StaticText(self.panel, -1, u'写代码:')

        self.commandText = wx.TextCtrl(self.panel, -1, u'')
        self.writePyText = wx.TextCtrl(self.panel, -1, u'''#-*-coding:utf-8-*-\n#python code here''',
                                  style=wx.TE_MULTILINE, size=(300, 200))

        self.send = wx.Button(self.panel, label=u'发送命令')
        self.clear = wx.Button(self.panel, label=u'清空命令')
        self.screen = wx.Button(self.panel, label=u'查看屏幕')
        self.refresh = wx.Button(self.panel, label=u'刷新')

        # self.serverList = ['192.168.0.4', '10.19.2.1', '192.168.0.111', '172.26.123.5', '192.168.6.11', '192.99.8.8']
        self.serverList = []
        self.server = wx.ListBox(self.panel, -1, size=(120, 100), choices=self.serverList, style=wx.LB_SINGLE)

        img = wx.Image(r'logo.jpg', wx.BITMAP_TYPE_ANY).Scale(200, 200)
        self.screenBox = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(img))

        self.Bind(wx.EVT_BUTTON, self.onSend, self.send)
        self.Bind(wx.EVT_BUTTON, self.onClear, self.clear)
        self.Bind(wx.EVT_BUTTON, self.onScreen, self.screen)
        self.Bind(wx.EVT_BUTTON, self.onRefresh, self.refresh)

        #基于GirdBagSizer布局
        self.gridBagSizerAll = wx.GridBagSizer(hgap=5, vgap=5)
        self.gridBagSizerAll.Add(self.server, pos=(0, 0),
                            flag=wx.ALL | wx.EXPAND,
                            span=(6, 2), border=5)
        self.gridBagSizerAll.Add(self.refresh, pos=(6, 0),
                            flag=wx.ALL | wx.EXPAND,
                            span=(1, 2), border=5)

        self.gridBagSizerAll.Add(commandStatic, pos=(0, 2),
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            border=5)
        self.gridBagSizerAll.Add(self.commandText, pos=(0, 3),
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            span=(1, 2), border=5)

        self.gridBagSizerAll.Add(writePyStatic, pos=(1, 2),
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            span=(1, 3), border=5)
        self.gridBagSizerAll.Add(self.writePyText, pos=(2, 2),
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            span=(4, 3), border=5)
        self.gridBagSizerAll.Add(self.send, pos=(6, 2),
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            span=(1, 1), border=5)
        self.gridBagSizerAll.Add(self.clear, pos=(6, 3),
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            span=(1, 1), border=5)
        self.gridBagSizerAll.Add(self.screen, pos=(6, 4),
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            span=(1, 1), border=5)

        self.gridBagSizerAll.Add(self.screenBox, pos=(0, 5),
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            span=(7, 2), border=5)

        self.panel.SetSizer(self.gridBagSizerAll)

        # self.SetSizeHints(250, 200, 700, 400) #设定窗口的最大最小值
        self.gridBagSizerAll.AddGrowableCol(0, 1)
        self.gridBagSizerAll.AddGrowableCol(1, 1)
        self.gridBagSizerAll.AddGrowableCol(2, 1)
        self.gridBagSizerAll.AddGrowableCol(3, 1)
        self.gridBagSizerAll.AddGrowableCol(4, 1)
        self.gridBagSizerAll.AddGrowableCol(5, 1)
        self.gridBagSizerAll.AddGrowableCol(6, 1)

        self.gridBagSizerAll.AddGrowableRow(0, 1)
        self.gridBagSizerAll.AddGrowableRow(1, 1)
        self.gridBagSizerAll.AddGrowableRow(2, 1)
        self.gridBagSizerAll.AddGrowableRow(3, 1)
        self.gridBagSizerAll.AddGrowableRow(4, 1)
        self.gridBagSizerAll.AddGrowableRow(5, 1)
        self.gridBagSizerAll.AddGrowableRow(6, 1)
        self.gridBagSizerAll.Fit(self)

    def onSend(self, event):
        server = self.server.GetSelection()
        if server != -1:
            slave = self.serverList[server]
            command = self.commandText.GetValue()
            writePy = self.writePyText.GetValue()
            if command:
                print u'输入的命令是: %s' % command
                self.masterSocket = MasterSocket(SERVER, PORT, command, commandType='commandInConfig', to=slave)
            elif writePy:
                self.masterSocket = MasterSocket(SERVER, PORT, writePy, commandType='commandInWrite', to=slave)
            else:
                print u'请输入命令'
                return None
            self.masterSocket.setDaemon(True)
            self.masterSocket.start()
        else:
            print u'请先选择被控端。'
            return None

    def onClear(self, event):
        self.commandText.Clear()
        self.writePyText.Clear()
        self.writePyText.AppendText(u'''#-*-coding:utf-8-*-\n#Python code here''')

    def onScreen(self, event):
        img = wx.Image(r'python.jpg', wx.BITMAP_TYPE_ANY).Scale(300, 200)
        self.screenBox.SetBitmap(wx.BitmapFromImage(img))
        self.gridBagSizerAll.Fit(self)

    def onRefresh(self, event):
        self.serverList = []

        socketForServerList = MasterSocket(SERVER, PORT, 'listSlave', self.serverList)
        socketForServerList.setDaemon(True)
        socketForServerList.start()
        socketForServerList.join()

        self.lock.acquire()
        print u'被控端列表111：%s' % str(self.serverList)
        self.server.Clear()
        for each in self.serverList:
            self.server.Append(each)
        self.lock.release()

if __name__ == "__main__":
    app = wx.App()
    frame = Slave()
    frame.Show()
    app.MainLoop()
