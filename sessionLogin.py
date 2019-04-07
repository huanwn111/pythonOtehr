#==session与cookie关系。模拟登录发评论优化cookie模拟 建req session类实例对象使用它的post方法保持cookies 登录时存到本地
# 用session会话整体模拟用户登录发评论系列操作==

import requests as req
import json

#创建req的seesion对象实例
sessionNew = req.session()

#print("11111111111111111")
#print(sessionNew)
headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' }

#登录函数
def loginFn():
    urlLogin = 'https://wordpress-edu-3autumn.localprod.forc.work/wp-login.php'
    dataLogin = {
        'log': input('请输入用户名：'),
        'pwd': input('请输入密码：'),
        'wp-submit': '登录',
        'redirect_to': 'https://wordpress-edu-3autumn.localprod.forc.work',
        'testcookie': 1
    }

    #登录
    #req.post(urlLogin, data=dataLogin, headers = headers)
    #req直接请求是上面，我们用req session类的实例对象 sessionNew的post方法，可保持cookie，评论时无需把.cookies取出来再传进去
    statusRs = sessionNew.post(urlLogin, headers = headers, data = dataLogin)
    if statusRs.status_code == 200:#【注意，前面是返回值.status_code，报错码只是返回值的一部分】
        print('登录成功')
        #把会话cookies由cookiesjar的格式转成字符串存入txt文件
        #用req.utils.dict_from_cookiejar()
        cookiesDict = req.utils.dict_from_cookiejar(sessionNew.cookies)#cookiesjar包格式转dict/json（可理解为解压）
        cookiesStr = json.dumps(cookiesDict)#dict/json转字符串
        with open(r'cookiesSL.txt','w') as fw:#存入本地
            fw.write(cookiesStr)
    else:
        print('登录失败，请检查')
    
#发评论
def writeCommentFn():

    urlComment = 'https://wordpress-edu-3autumn.localprod.forc.work/wp-comments-post.php'
    
    dataComment = {
        'comment': input('请输入评论内容：'),
        'submit': '发表评论',
        'comment_post_ID': '7',
        'comment_parent': '0'
    }

    #用req session 类的 实例对象 sessionNew的post方法 发评论请求，不用传cookies，当前会话已保持(携带)cookies
    rs = sessionNew.post(urlComment, headers=headers, data=dataComment)
    #print("22222222222")
    #print(rs)
    return (rs)#加()组成一个整体元组格式

#存本地cookies
def readCookiesFn():

    with open(r'cookiesSL.txt','r') as fr:

        cookiesStr = fr.read()#读出cookies字符串
        cookiesDict = json.loads(cookiesStr)#字符串转json格式
        cookiesJar = req.utils.cookiejar_from_dict(cookiesDict)#dict/json格式转cookiejar包格式，给会话用（可理解为打包）。#用req utils cookiejar_from_dict
        #print("333333333333333")
        #(cookiesJar)

        return (cookiesJar)#加()组成一个整体元组格式


#读取更新会话最新cookies
try:#正常本地读
    sessionNew.cookies = readCookiesFn()
except FileNotFoundError:#读不到则需登录，并记录存储cookies到本地（login中完成了存）
    loginFn()#登录
    #更新最新会话cookies（即使是刚存到本地的，也要从统一的入口--
    sessionNew.cookies = readCookiesFn()

#发评论
#【以下这种判断cookie过期的方法是不对的，请求不成功有可能是cookie没过期，其它原因，比如发评论时429，请求过多之类的】
rsWrite = writeCommentFn()#执行并返回状态码
if rsWrite.status_code == 200:#请求成功.【注意前面是rsWrite.status_code，报错码只是返回值的一部分】
    print("发表成功！～")
else:#请求失败，则说明cookies过期，重新登录->并且发评论
    loginFn()
    status = writeCommentFn()



#==【重要重要：cookie和session的关系：
#cookie记录用户浏览行为，session会话为服务器端记录用户行为。
# 为了让信息同步（在不同网页间确定是同一个用户在做着一个会话，或记住密码，隔天付款购物车等）
# 通过cookie里的session的id关联）】==
#===============【思路】================
#==创建reqests的会话(session)实例对象 sessionNew = req.session()
#==【重点概念：req的session对象（就像服务器的session，并不是一个，注意），
# 可以跨请求保持参数，
# 可以同一个Session实例发出的所有请求之间保持cookie，
# 所以可以连接会被重用，性能提升】
# 它有.post .get方法，用法同req.post .get
# 重点是：cookie不用传了，打印res.text看下，
    # session对象请求在session.post 登录请求这一步就存在这个会话实例中保持下去了，
    # 发评论时就不用再.cookies取出来再传进去了。
# 不过要做件事，登录后把.cookies存到txt，
    # 用于下次访问时去里面找cookie，找到则不用登录（相当于密码记住在了cookie里）
    # 找不到则登录->存cookie（把该会话实例sessionNew.cookies转成字符串存入txt文件）->评论，
# //try except里面函数执行随时更新全局sessionNew.cookies
    # (包括初次登录后也要更新，登录函数里存cookie归存cookie，
    # 但还是要从刚存的里面读出来最新的会话cookies供整个会话使用)==
#//session过期判断：根据评论失败（status_code非200）则重新登录->更新最新会话cookies->发评论
#注意：【请求返回值.status_code取返回值是否成功码。】
#return ()返回一个整体元组。




