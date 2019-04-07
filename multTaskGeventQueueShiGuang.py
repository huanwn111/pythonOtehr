
#用gevent queue 并发多协程 多任务队列 概念 爬取时光网电视剧
#import requests as req#【这种带as的最好另起一行，逗号拼的第一遍运行会报错】
#【打开csv不用在任务里每次重新打开一个，在全局定义，这里用writer就可以】
#【遗留问题：进程阻塞】
import requests as req
from bs4 import BeautifulSoup as BS
import csv
from gevent import monkey
monkey.patch_all()
import gevent,time
from gevent.queue import Queue

#csv文件加标题栏
with open(r'multTaskShiGuang.csv','a+',newline='',encoding='utf-8') as fwCsv:
    csvWriter = csv.writer(fwCsv)
    csvWriter.writerow(['剧名','导演','演员','简介'])

#==创建请求队列==
quGroup = Queue()
urlList = [
    'http://www.mtime.com/top/tv/top100/',
    'http://www.mtime.com/top/tv/top100/index-1.html',
    'http://www.mtime.com/top/tv/top100/index-2.html',
    'http://www.mtime.com/top/tv/top100/index-3.html',
    'http://www.mtime.com/top/tv/top100/index-4.html',
    'http://www.mtime.com/top/tv/top100/index-5.html',
    'http://www.mtime.com/top/tv/top100/index-6.html',
    'http://www.mtime.com/top/tv/top100/index-7.html',
    'http://www.mtime.com/top/tv/top100/index-8.html',
    'http://www.mtime.com/top/tv/top100/index-9.html',
    'http://www.mtime.com/top/tv/top100/index-10.html'
]

for item in urlList:#请求压入队列
    quGroup.put_nowait(item)

#==建立单个爬取任务== 
def singleTaskFn():
    while not quGroup.empty():#别忘了加非空判断
        #取队列中的请求
        urlSingle = quGroup.get_nowait()
        #处理请求
        resSingle = req.get(urlSingle)
        htmlTag = BS(resSingle.text)
        rowBox = htmlTag.find_all('div',class_='mov_con')
        with open(r'multTaskShiGuang.csv','a+',newline='',encoding='utf-8') as fwCsv:
            csvWriter = csv.writer(fwCsv)
            #csvWriter.writerow(['剧名'])
            #【打开csv不用在任务里每次重新打开一个，在全局定义，这里用writer就可以】
            for row in rowBox:
                name = row.find('h2').text
                director = row.find_all('p')[0].text#第0个p标签，注意前面是find_all
                actor = row.find_all('p')[1].text
                info = row.find_all('p')[2].text
                print([name,director,actor,info])            
                csvWriter.writerow([name,director,actor,info])

#==创建任务==
taskList = []
for i in range(11):#抓10页，建10个任务
    #gevent.sleep(1)
    #防止进行spawn不到join不起来，发生阻塞，报错gevent.exceptions.LoopExit: This operation would block forever
    #解决方法参考：http://xiaorui.cc/2016/08/07/%E5%85%B3%E4%BA%8Egevent-queue%E9%81%AD%E9%81%87hub-loopexit%E9%97%AE%E9%A2%98/
    taskItem = gevent.spawn(singleTaskFn)
    taskList.append(taskItem)

#==执行任务==
gevent.joinall(taskList)




