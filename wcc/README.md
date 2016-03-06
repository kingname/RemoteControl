#WCC v0.1

##介绍/Introduce

WCC（Web Control Computer）是一个通过网页控制电脑的程序，用户可以在网页上下达命令，安装了客户端的电脑将会执行命令。下命令的方式分为两种，预定义命令和直接写入Python代码。

##安装与配置/Install and config

###客户端

####_config.ini

对v0.1版本，客户端直接读取服务器上的MongoDB来获取数据，因此需要配置服务器的域名和端口。

	[Server]
	host = xxxx.com
	port = 27017

其中host填写服务器的域名或者IP地址，port填写MongoDB的端口，默认是27017.

	[Client]
	timelimit = 10

客户端采用轮询的方式查询数据库，timelimit设定轮询的时间间隔，默认为10，单位为秒。

	[Command]
	shutdown=shutdown -f -s -t 10 -c closing...
	dir=dir
	
	#打开文件，文件名不能为中文,不要有空格
	[Open]
	music = F:\backup\Music\Intro.mp3
	notepad = notepad

这一段设定预定义的命令。

[Command]下面的命令是使用CMD来执行。

[Open]下面的命令是使用win32api来执行。等号左侧是命令的名字，右侧是具体命令。

设定好以后，运行wcc.py:

	python wcc.py

###网页端

对于网页端来说，需要注意的是，要允许从外部访问MongoDB。

需要直接运行webControl.py：

	python webControl.py

##使用/Usage

打开网页端如图：

![](http://7sbpmp.com1.z0.glb.clouddn.com/wcc.png)

其中**内置命令** 这一项可以填写在_config.ini中定义的命令。**直接写代码**下面，可以直接贴Python的代码，格式和缩进会自动保留。

填写完成以后，点击**发送命令**按钮，10秒内，远程电脑上就会执行命令了。



##视频课程

[Flask 快速搭建网站](http://www.jikexueyuan.com/course/2348.html)

[网页控制电脑](http://www.jikexueyuan.com/course/2389.html)