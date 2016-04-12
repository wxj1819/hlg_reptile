#! /usr/bin/env python
#coding=utf-8
import urlread,sendmail
import datetime,time,os


SECONDS_PER_DAY = 24*60*60 

def doFunc(logfile):
    mailto_list=['******@qq.com','********@qq.com']#收邮件人列表
    #record_log(logfile,'有','邮件投递成功')
    time.sleep(doFirst())
    xtfw=urlread.getxtfw()
    jwzx=urlread.getjwzx()
    dy2018=urlread.getdy2018()
    ismessage=(int(xtfw!='')|int(jwzx!='')|int(dy2018!=''))
    content=''#清空变量
    if int(jwzx!=''):
        content=('<p>以下是今天的教务在线更新信息：</p>%s<p>&nbsp;</p>' %jwzx) #<p></p>
    if int(xtfw!=''):
        content=('%s<p>以下是今天的“校园综合协调服务管理平台”最新信息：</p>%s<p>&nbsp;</p>' %(content,xtfw))
        content=('%s<p><a href="http://202.118.201.228/homepage/index.do">教务在线首页</a></p>'%content)
    if int(dy2018!=''):
        content=('%s<p>电影天堂电影更新：</p>%s<p>&nbsp;</p>' %(content,dy2018))

    if ismessage:
        content=('%s<p><a href="mailto:*******@qq.com">如需取消，请点这里</a></p>'%content)
        content=('%s<p>***********</p><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;By wxj</p>'%content)
        
        #print(content)

        if sendmail.send_mail(mailto_list,"教务在线有新消息了！",content,'html'):
            #print ("邮件投递成功")
            record_log(logfile,ismessage,'邮件投递成功')
        else:  
            #print ("邮件投递失败")
            record_log(logfile,ismessage,'邮件投递失败')
        #print ("do well!")
    else:
        record_log(logfile,ismessage,'无邮件投递')


def doFirst():
    from datetime import datetime,timedelta
    dotime=[18,0,0,0]
    curTime = datetime.now()
    desTime = curTime.replace(hour=dotime[0],minute=dotime[1], second=dotime[2], microsecond=dotime[-1])
    delta = desTime - curTime
    if delta.total_seconds()<0:
        desTime=curTime.replace(day=(curTime.day+1),hour=dotime[0], minute=dotime[1], second=dotime[2], microsecond=dotime[-1])  
        delta = desTime - curTime
    #print(delta,'\t',delta.total_seconds())
    skipSeconds = delta.total_seconds()
    print ("The next time %s will do ,Must sleep %d seconds" %(desTime,skipSeconds))
    return skipSeconds


#记录日志函数
def record_log(filename,ismessage,email_status):
    if os.path.isfile(filename):
        f=open(filename,'a')
    else:
        f=open(filename,'a')
        f.write('Date\t   Time\t    Ismessage\t  email_status\n')
    nowtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    f.write('%s\t%s\t\t\t  %s\n'%(nowtime,ismessage,email_status))
    f.flush()
    f.close

#record_log('a.log','有','邮件投递成功')




nowtime=time.strftime("%Y%m%d_%H%M%S",time.localtime())
logfile='hlg_%s.log' %nowtime
while True:
    doFunc(logfile)

