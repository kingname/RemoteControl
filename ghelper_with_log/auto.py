#-*-coding:utf-8 -*-

import smtplib
import sys
from email.mime.text import MIMEText

reload(sys)
sys.setdefaultencoding('utf-8')

username = "123@sina.com"# 接收邮箱
password = "123abc"# 接收邮箱密码
mailbox = "greensouth@foxmail.com" #国内邮箱二

def send_mail(subject,body='Success'):
        msg = MIMEText(body,'plain','utf-8')#中文需参数‘utf-8’，单字节字符不需要
        msg['Subject'] = subject
        msg['from'] = username
        handle = smtplib.SMTP('smtp.sina.com', 25)
        handle.login(username,password)
        handle.sendmail(username,mailbox, msg.as_string())
        handle.close()