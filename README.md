MCC
===

Mail Control Computer

##目的：
本程序通过邮件控制电脑。

##原理：
Python使用Poplib库，周期性访问邮箱，根据邮件主题的相应名称执行对应的操作。

目前奴隶邮箱（Python检查的那个邮箱，简称奴隶邮箱）使用sina邮箱测试成功，其他邮箱未做测试。
主人邮箱（发送命令的邮箱称为主人邮箱），通过发送邮件给奴隶邮箱来控制操作。目前测试使用QQ邮箱与使用微信发送的QQ邮件能测试通过。

##配置
打开_config.ini文件:

###Slave

* pophost填写奴隶邮箱的pop3服务器，例如新浪的pop3服务器为
	
		pop.sina.com
*smtphost填写奴隶邮箱的SMTP服务器，例如新浪的SMTP服务器为

	    smtp.sina.com

* username为奴隶邮箱的邮箱号
* password为奴隶邮箱的密码
* 必须要先在新浪邮箱的账户控制中允许客服端收件，并打开POP3和SMTP协议，否则会出错。如图所示：
![](http://7sbpmp.com1.z0.glb.clouddn.com/QQ截图20150630000146.png)

###Boss
* mail为主人邮箱号
* timelimit控制程序检查邮箱的评论，默认为300秒，也就是5分钟

###Command
这个section的内容是可以使用Python运行的cmd命令，理论上讲，任何Python可以执行的命令都可以添加到这里。
		名字 = 命令

###Open
这个section下的内容为可以通过Python打开的文件或者内容，例如打开记事本，打开音乐等等。
		名字 = 地址

##使用
使用主人邮箱往奴隶邮箱发送邮件，标题为_config.ini中的任一命令的**名字**（等号左边的内容）。例如，想打开记事本，那就使用邮箱发送标题为notepad的邮件。

##编译
	python mysetup.py py2exe
