#!/usr/bin/python3

import urllib.request
from bs4 import BeautifulSoup,Tag
import re
import os,sys,time,datetime
import sendmail

def getxtfw():#爬取学校反馈网站
    #mailto_list=['*****@qq.com'] #
    url="http://202.118.201.17/xtfw/"
    #url="http://www.hrbust.edu.cn/"
    #url="http://www.gxnu.edu.cn/default.html"
    data=urllib.request.urlopen(url).read()
    page_data=data.decode('utf-8')
    #print(page_data)
    soup=BeautifulSoup(page_data,"lxml")
    
    href=re.compile('(UI\/showFinished\.aspx\?BH\=\w{8}-\w{4}-\w{4}-\w{4}-\w{12})')
    i=0
    content_all=''
    for link in soup.findAll('li'):#get all links of gxnu index  ['href'],link.contents   
        for link in link.findAll('a'):#使用正则表达式
            i=i+1
            #print(link,'\n')
            href=re.compile('(UI\/showFinished\.aspx\?BH\=\w{8}-\w{4}-\w{4}-\w{4}-\w{12})')
            res=url+','.join(href.findall(str(link)))
            title=','.join(link.contents)
            if i>10:
                print('已处理问题%d：'%(i-10),title)#显示标题
            else:
                if i==10:
                    print('未处理问题%d：'%i,title)#显示标题
                    print('\n')
                else:
                    print('未处理问题%d：'%i,title)#显示标题
            #print(','.join(link.contents),'\n',res)#显示标题和网址

            #查找最近发布的消息
            date=re.compile('\d{4}年\d{1,2}月\d{1,2}日')
            push_time=(','.join(date.findall(title)))#发文时间
            
            #print(push_time)
            date1=re.compile('\d+')
            push_time=(date1.findall(push_time))#提取纯数字时间
            
            push_time=datetime.datetime(int(push_time[0]),int(push_time[1]),int(push_time[2]))#发布时间，时间格式
            
            cur_time=datetime.datetime.now()#获得当前的时间
            '''设置时间限制'''
            if (cur_time-push_time).days<=2:#抓取新发布的消息内容
                
                data=urllib.request.urlopen(res).read()
                page_data=data.decode('utf-8')
                #print(page_data)
                soup=BeautifulSoup(page_data,"lxml")
                for link in soup.findAll('textarea',id="NeiRong"):
                    print('反馈内容：\n',','.join(link.contents))#显示反馈内容
                    contents="<p><a href='%s'>%s</a></p><p>%s</p>" %(res,title,(''.join(link.contents)))
                    #print(contents)
                for links in soup.findAll('textarea',id="fbContent"):
                    xxcontenets=','.join(links.contents)
                    if xxcontenets!='':
                        contents="%s<p>官方回应：</p><p>%s</p>" %(contents,xxcontenets)
                        #print('官方回应：\n',xxcontenets,'\n')#显示学校回应内容
                    content_all='%s%s'%(content_all,contents)
    #print(content_all,'\n\n')
    return content_all

def getjwzx():
    #mailto_list=['*****@qq.com']
    url="http://202.118.201.228/homepage/infoArticleList.do;jsessionid=62FB09BBADF2968A056DD9D24FB58067.TH?columnId=354"
    #教务在线教务公告列表
    url2="http://202.118.201.228/homepage/"
    data=urllib.request.urlopen(url).read()
    page_data=data.decode('utf-8')
    #print(page_data)
    soup=BeautifulSoup(page_data,"lxml")
    #print(soup)
    message=''
    for li in soup.findAll('li'):
        for link in li.findAll('a',href=re.compile('infoSingleArticle\.do\?articleId\=\d{4}\&columnId\=354'),target="_blank"):
            url3=url2+link['href']
            title=link.get_text().strip()
            
            #print(title,'\t',''.join(li.span.contents))#新闻标题、新闻发出时间
            #print(url3)#网址
            
            temp=''.join(li.span.contents).split('-')
            push_time=datetime.datetime(int(temp[0]),int(temp[1]),int(temp[2]))#发布时间，时间格式
            cur_time=datetime.datetime.now()#获得当前的时间
            days=(cur_time-push_time).days
            if days<=1:#抓取新发布的消息内容
                print(title,'\t',''.join(li.span.contents),'\t',days)#新闻标题、新闻发出时间
                print(url3)#网址
                content_temp="<p><a href='%s'>%s</a></p>" %(url3,title)
                message=message+''.join(content_temp)
                #print(content_temp)
    return message

def getdy2018():
    url="http://www.dy2018.com"
    #获取电影天堂电影列表
    data=urllib.request.urlopen(url).read()
    page_data=data.decode('GBK')
    #print(page_data)
    soup=BeautifulSoup(page_data,"lxml")
    #print(soup)
    message=''
    dymtitle=[]#存放电影模块标题
    for ul in soup.findAll('div',class_='title_all'):
        dymtitle.append(''.join(ul.get_text().strip().replace('更多>>','')))
    #print(dymtitle[0])
    i=0#记录电影所属模块
    n=0#标记是否有电影更新
    for ul in soup.findAll('div',class_='co_content222'):
        #print(dymtitle[i])
        message='%s<p>%s</p>' %(message,dymtitle[i])
        #print(message)
        i=i+1
        for li in ul.findAll('li'):

            if li.span!=None:
                nowdate=time.strftime("%m-%d",time.localtime())
                #yestoday='%s-%s'%(time.localtime()[1],time.localtime()[2]+1)
                if nowdate==(li.span.get_text().strip()):#更新时间为今天
                    #print(nowdate)
                    for link in li.findAll('a',href=re.compile(r'/i/\d+.html')):
                        #print(link)
                        dytitls=link.get_text().strip()#电影标题
                        #print(dytitls)

                        dyurl='%s%s'%(url,link['href'])#电影链接
                        #print(dyurl)

                        #爬每一部电影
                        data=urllib.request.urlopen(dyurl).read()
                        page_data=data.decode('GBK')
                        #print(page_data)
                        soup=BeautifulSoup(page_data,"lxml")
                        for scores in soup.findAll('strong',class_="rank"):#爬每部电影分数
                            score=scores.get_text().strip()
                            #print(score)
                        for mlinks in soup.findAll('td',style="WORD-WRAP: break-word",bgcolor="#fdfddf"):#爬磁力链接
                            mlink=mlinks.get_text().strip()
                            #print(mlink)
                        if float(score)>=5:#设置电影分数限制
                            n=n+1
                            message=message+"<p><a href='%s'>%s</a>&nbsp;%s</p><p><a href='%s'>点此下载</a></p>" %(dyurl,dytitls,score,mlink)
        #print('\n')
    if n==0:
        return ''
    else:
        #print(message)
        return message


#函数调用
#print(getxtfw())
#print(getjwzx())
#print(getdy2018())
#getdy2018()



'''
import urllib.request
from bs4 import BeautifulSoup
import re

def getgxnu():
    url="http://www.gxnu.edu.cn/default.html"
    data=urllib.request.urlopen(url).read()
    page_data=data.decode('GBK')
    #print(page_data)
    soup=BeautifulSoup(page_data)
    #for link in soup.findAll('a',target='_self'):#get all links of gxnu index
    #    print(link)
    for link in soup.findAll('a',href=re.compile('http://\\S+/type/\\d+.html')):#使用正则表达式
        print(link['href'],link.contents)
        
    
#函数调用
getgxnu()
'''

