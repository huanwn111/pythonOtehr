#schedule.every().friday.at("09:00").do(main)
#星期后面没() 小写，seconds hour也没,do里面的函数没括号，注意。时间格式两位，不足补0

import requests
from bs4 import BeautifulSoup
import smtplib 
from email.mime.text import MIMEText
from email.header import Header
import schedule#小写，注意

fromAddr = input('输入发件箱')
password = input('输入授权码')

def getFood():
    res_foods = requests.get('http://www.xiachufang.com/explore/')
    bs_foods = BeautifulSoup(res_foods.text,'html.parser')
    list_foods = bs_foods.find_all('div',class_='info pure-u')

    #list_all = []
    n = 0
    listTest = ''
    for food in list_foods:
        n = n+1
        tag_a = food.find('a')
        name = tag_a.text[17:-13]
        URL = 'http://www.xiachufang.com'+tag_a['href']
        tag_p = food.find('p',class_='ing ellipsis')
        ingredients = tag_p.text[1:-1]
        #list_all.append([name,URL,ingredients])
        listTest += str(n)+name+"\n"+URL+"\n"+ingredients+"\n"+"--------------\n"
    return listTest

def sendMail(content):

    host='smtp.qq.com'
    toAddr = fromAddr
    content = content#邮件内容

    #创建邮件对象
    try:
        mailObj = smtplib.SMTP_SSL(host,465)
    except:
        print('连接邮件服务器不成功')
    #登录
    try:
        mailObj.login(fromAddr,password)
    except:
        print('登录不成功')
    
    #封装处理邮件内容标题等（MIMEText针对文本 plain普通 utf-8格式）
    msg = MIMEText(content,'plain','utf-8')
    msg['Subject'] = Header('本周最受欢迎菜谱定时发送','utf-8')
    msg['From'] = Header(fromAddr,'utf-8')
    #发邮件
    try:
        mailObj.sendmail(fromAddr,toAddr,msg.as_string())
        print("已发送，请查收")
    except:
        print("发送不成功，请检查")
    #关闭邮件服务器
    mailObj.quit()


def main():    
    foodRs = getFood()
    print(foodRs)
    sendMail(foodRs)


#定时执行
schedule.every().friday.at("09:00").do(main)#星期后面没()，seconds hour也没,do里面的函数没括号，注意。时间格式两位，不足补0

while True:
    schedule.run_pending()


    
