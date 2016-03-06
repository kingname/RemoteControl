##UIControl
####介绍

这个项目是我在极客学院《图形化远程控制程序》课程的配套程序，如果你想了解这个程序的运行原理，请访问最下面的课程链接观看我对这个程序的讲解。或者你也可以自行阅读程序的源代码。



##如何使用

程序分为三个部分，服务器端，控制端和被控端。

###服务器端
服务器端对应的的文件为server/Server.py, 如果你需要在公网环境下控制远程的电脑，请将服务器端部署在公网环境下的电脑中。运行服务器端不需要进行任何配置，只需要运行Server.py:

	python Server.py

simpleServer.py是一个socket的demo, 你可以阅读它的代码来更好的理解socket的实现方法。


##控制端

控制端对应的文件为client_Master/Master.py, 如果要使用控制端，请使用任何文本编辑器打开Master.py, 并将第7行SERVER的值设定为服务器端的公网IP地址，然后运行:

	python Master.py

由于控制端有图形界面，因此请安装wxPython.



##被控端

被控端对应的文件为client_Slave/Slave.py，请使用任何文本编辑器打开_config.ini，其中[Server]下面的host配置为服务器端的公网IP地址[Client]下面的timeout表示Socket连接超时的时间，你可以自行设定。[Command]和[Open]下面的内容为配置的各种命令，左侧是命令的名称。不同点在于[Command]使用os.system运行命令，[Open]使用Win32Api来运行命令。

	python Slave.py

如果你的操作系统不是Windows或者你没有安装Win32Api, 请修改client_Slave/util/excutor.py， 将

	import win32api

和所有与win32有关的代码注释掉，同时不能再使用[Open]下面的命令。



###隐藏窗口

在section3下面的代码演示了如何隐藏windows的cmd窗口，由于这个功能有木马性质，因此我不会将它集成到被控端里面，如果你有这个需要，你可以自行将代码集成进去。



##视频课程

[Python 图形程序入门](http://www.jikexueyuan.com/course/2553.html)

编写图形界面的远程控制程序（近期上线）

开发远程控制程序高级功能（近期上线）

