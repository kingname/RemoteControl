#-*-coding:utf-8 -*-

import poplib
import smtplib
import time
import os,sys
import re
import win32api
from email.mime.text import MIMEText
import logging

__Author__ = 'kingname'
__Verson__ = 0.1

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                datefmt='%Y %m %d %H:%M:%S',
                filename='auto.log',
                filemode='a')

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
        logging.info(u'开始登录邮箱')
        try:
                pp = poplib.POP3_SSL(host)
                pp.set_debuglevel(1)
                pp.user(username)
                pp.pass_(password)
                ret = pp.list()
                logging.info(u'登录邮箱成功。')
        except Exception,e:
                logging.error(e)
                exit()

        logging.info(u'开始抓取邮件。')
        try:
        down = pp.retr(len(ret[1]))
                logging.info(u抓取邮件成功。'')
        except Exception,e:
                logging.error(e)
                exit()

        logging.info(u'开始抓取subject和发件人')
        try:
                subject = re.search("Subject: (.*?)',",str(down[1]).decode('utf-8'),re.S).group(1)
                sender = re.search("'X-Sender: (.*?)',",str(down[1]).decode('utf-8'),re.S).group(1)
                logging.info(u'抓取subject和发件人成功')
        except Exception,e:
                logging.error(e)
                exit()

        if subject != 'pass':
                if sender == boss_email:
                        DealCommand(subject)
        pp.quit()

def DealCommand(subject):
        logging.info(u'开始处理命令。')
        send_mail('pass','slave')
        if subject in command_dict:
                logging.info(u'执行命令')
                try:
                        command = command_dict[subject]
                        os.system(command)
                        send_mail('Success','boss')
                        logging.info(u'执行命令成功')
                except Exception,e:
                        logging.error(e)
                        send_mail('error','boss',e)
        elif subject in open_dict:
                logging.info(u'打开文件')
                try:
                        open_file = open_dict[subject]
                        win32api.ShellExecute(0, 'open', open_file, '','',1)
                        send_mail('Success','boss')
                        logging.info(u'打开文件成功')
                except Exception,e:
                        logging.error(e)
                        send_mail('error','boss',e)
        else:
                send_mail('error','boss','no such command')


def send_mail(subject,flag,body='Success'):
        
        msg = MIMEText(body,'plain','utf-8')#中文需参数‘utf-8’，单字节字符不需要
        msg['Subject'] = subject
        msg['from'] = username
        logging.info('开始配置发件箱。')
        try:
                handle = smtplib.SMTP('smtp.sina.com', 25)
                handle.login(username,password)
                logging.info('发件箱配置成功')
        except Exception,e:
                logging.error(e)
                exit()

        logging.info(u'开始发送邮件'+ 'to' + flag)
        if flag == 'slave':
                try:
                        handle.sendmail(username,username, msg.as_string())
                        logging.info(u'发送邮件成功')
                except Exception,e:
                        logging.error(e)
                        exit()
        elif flag == 'boss':
                try:
                        handle.sendmail(username,boss_email, msg.as_string())
                        logging.info(u'发送邮件成功')
                except Exception,e:
                        logging.error(e)
                        exit()
                
        handle.close()
        logging.info(u'发送邮件结束'+flag)

#读取配置文件
def init():
        global username,password,host,boss_email,time_limit
        try:
                f = open('_config.ini','r')
        except IOError,e:
                logging.error(e)
                exit()

        info = f.readlines()
        try:
                host = re.search('host:(.*?)\n',info[0],re.S).group(1)
                username = re.search('username:(.*?com)',info[1],re.S).group(1)
                password = re.search('password:(.*?)\n',info[2],re.S).group(1)
                boss_email = re.search('boss_email:(.*?com)',info[3],re.S).group(1)
                time_limit = re.search('time_limit:(.*?)\n',info[4],re.S).group(1)
        except Exception,e:
                logging.error(e)
        logging.info(u'打开配置文件成功。。。')


        #将命令生成字典，便于查询
        command_start = info.index('<command>\n')
        command_end = info.index('</command>\n')
        for each in info[command_start+1:command_end]:
                command = each.split('=')
                command_dict[command[0]] = command[1]
        logging.info(command_dict)

        open_start = info.index('<open_file>\n')
        open_end = info.index('</open_file>\n')
        for each in info[open_start+1:open_end]:
                open_file = each.split('=')
                open_dict[open_file[0]] = open_file[1][:-1]
        logging.info(open_dict)
        f.close()


if __name__=='__main__':
        init()
        print u'等待接收命令'
        logging.info(u'初始化完成。')
        while 1:
                time.sleep(int(time_limit)) #每5分钟检查一次邮箱
                accp_mail()


