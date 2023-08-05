#-*- coding:utf-8 -*-
'''
提供邮件收发模块
'''
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
def send_email(email_config, body):
        ret = True
        try:
            msg = MIMEText(body["body"], body["type"], 'utf-8')
            msg['From'] = formataddr(["", email_config["sender"]])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号

            msg['To'] = formataddr(body["receivers"])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = body["title"]  # 邮件的主题，也可以说是标题
            server = smtplib.SMTP_SSL(email_config["host"], email_config["port"])  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(email_config["sender"], email_config["pwd"])  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(email_config["sender"], body["receivers"], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
            print("邮件发送成功")
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret = False
            print("邮件发送失败")
        return ret

def get_email():
    pass
