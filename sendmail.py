#
# -*- coding: UTF-8 -*-
'''
发送txt文本邮件
'''
import smtplib  
from email.mime.text import MIMEText  
mailto_list=['****@qq.com','*****@qq.com'] #
'''
mail_host="smtp.qq.com"  #设置服务器
mail_user="******"    #用户名
mail_pass="*******"   #口令 
mail_postfix="qq.com"  #发件箱的后缀
'''
mail_host="smtp.163.com"  #设置服务器
mail_user="*******"    #用户名
mail_pass="******"   #口令 
mail_postfix="163.com"  #发件箱的后缀

def send_mail(to_list,sub,content,mailtype='plain'):  
    me="王晓俊"+"<"+mail_user+"@"+mail_postfix+">"
    if mailtype=='plain':
        msg = MIMEText(content,_subtype='plain',_charset='utf-8')
    elif mailtype=='html':
        msg = MIMEText(content,_subtype='html',_charset='utf-8')
    else:
        return False
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ",".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)
        #server.starttls() ##
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True
    except Exception as e: 
        print (str(e))  
        return False
'''
#构造附件1
att1 = MIMEText(open('d:\\123.rar', 'rb').read(), 'base64', 'gb2312')
att1["Content-Type"] = 'application/octet-stream'
att1["Content-Disposition"] = 'attachment; filename="123.doc"'#这里的filename可以任意写，写什么名字，邮件中显示什么名字
msg.attach(att1)
'''    
if __name__ == '__main__':  
    if send_mail(mailto_list,"反馈信息","<a href='http://www.baidu.com'>打扰了</a>",'html'):
    
        print ("发送成功")  
    else:  
        print ("发送失败")
		
#send_mail(mailto_list,'test','nihao ')

        

