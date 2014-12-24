#-*-coding:utf-8 -*-

import poplib
import smtplib
import time
import os,sys
import re
import win32api
from email.mime.text import MIMEText

reload(sys)
sys.setdefaultencoding('utf-8')

host = "" #邮箱的pop3服务器
username = ""# 接收邮箱
password = ""# 接收邮箱密码
boss_email = "" #控制邮箱
time_limit = 300

command_dict = {}
open_dict = {}
 
def accp_mail():

        pp = poplib.POP3_SSL(host)
        pp.set_debuglevel(1)
        pp.user(username)
        pp.pass_(password)
        ret = pp.list()
        down = pp.retr(len(ret[1]))
        subject = re.search("Subject: (.*?)',",str(down[1]).decode('utf-8'),re.S).group(1)
        sender = re.search("'X-Sender: (.*?)',",str(down[1]).decode('utf-8'),re.S).group(1)
        if subject != 'pass':
                if sender == boss_email:
                        DealCommand(subject)
        pp.quit()

def DealCommand(subject):
        send_mail('pass','slave')
        if subject in command_dict:
                command = command_dict[subject]
                try:
                        os.system(command)
                        send_mail('Success','boss')
                except Exception as e:
                        send_mail('error','boss',e)
        elif subject in open_dict:
                open_file = open_dict[subject]
                try:
                        win32api.ShellExecute(0, 'open', open_file, '','',1)
                        send_mail('Success','boss')
                except Exception as e:
                        send_mail('error','boss',e)
        else:
                send_mail('error','boss','no such command')


def send_mail(subject,flag,body='Success'):
        msg = MIMEText(body,'plain','utf-8')#中文需参数‘utf-8’，单字节字符不需要
        msg['Subject'] = subject
        msg['from']='kingname_auto0@sina.com'
        handle = smtplib.SMTP('smtp.sina.com', 25)
        handle.login(username,password)
        if flag == 'slave':
                handle.sendmail(username,username, msg.as_string())
        elif flag == 'boss':
                handle.sendmail(username,boss_email, msg.as_string())
                #发送
        handle.close()

#读取配置文件
def init():
        global username,password,host,boss_email,time_limit
        f = open('_config.ini','r')
        info = f.readlines()
        host = re.search('host:(.*?)\n',info[0],re.S).group(1)
        username = re.search('username:(.*?com)',info[1],re.S).group(1)
        password = re.search('password:(.*?)\n',info[2],re.S).group(1)
        boss_email = re.search('boss_email:(.*?com)',info[3],re.S).group(1)
        time_limit = re.search('time_limit:(.*?)\n',info[4],re.S).group(1)


        #将命令生成字典，便于查询
        command_start = info.index('<command>\n')
        command_end = info.index('</command>\n')
        for each in info[command_start+1:command_end]:
                command = each.split('=')
                command_dict[command[0]] = command[1]

        open_start = info.index('<open_file>\n')
        open_end = info.index('</open_file>\n')
        for each in info[open_start+1:open_end]:
                open_file = each.split('=')
                open_dict[open_file[0]] = open_file[1][:-1]
        f.close()

if __name__=='__main__':
        init()
        while 1:
                time.sleep(time_limit) #每5分钟检查一次邮箱
                accp_mail()


