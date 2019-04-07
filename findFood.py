#session cookie模拟登录爬吃的等系列用户行为，输入验证码图片验证码处理 登录请求preserve log
#==【重要重要：cookie和session的关系：
#cookie记录用户浏览行为，session会话为服务器端记录用户行为。
# 为了让信息同步（在不同网页间确定是同一个用户在做着一个会话，或记住密码，隔天付款购物车等）
# 通过cookie里的session的id关联）】==
#本例的session是指reqeusts session类的实例对象，可携带cookie，有post get等方法 传参一站请求即可。
#本例用到输入手机验证码：把每一步请求操作理解成人在手动操作网页就不难理解了。
#登录请求是怎么找到的？页面正常登录勾选network里Preserve log,完成登录后即可找到。Preserve log可保障不会登录后跳走消息这个请求
#【取到的json取值时 注意json转字典再取.json()['键名']，不要习惯性直接取了】
#图片验证码取到的 base64编码要split一下，逗号后面是，前面加了标识
#//要知道本例中这些爬取的用户行为初次接触有点陌生，但都是很初级很常用的，战略上藐视它。

import requests as req
import json
import base64

#创建会话（req session类的实例对象），在本会话内登录及换页请求爬取
sessionNew = req.session()

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

#登录函数
def loginFn():
    tel = input('请输入手机号')
    '''
    #==取验证码=
    urlToken = 'https://h5.ele.me/restapi/eus/login/mobile_send_code'

    dataToken = {
        "captcha_hash":"",
        "captcha_value":"",
        "mobile":tel,
        "scf":"ms"
    }
    tokenTel = sessionNew.post(urlToken,headers=headers,data=dataToken)
    #取得tokenTel手机验证码后，传入登录请求的validate_code即可。
    '''
    #但是（由于多次输入被禁，需要输入图形验证码）,如下处理：

    #==取图形验证码==
    urlTokenImg = 'https://h5.ele.me/restapi/eus/v3/captchas'
    dataTokenImg = {
        "captcha_str":tel
    }
    tokenImgDatas = sessionNew.post(urlTokenImg,headers=headers,data=dataTokenImg)
    tokenImg64Code = tokenImgDatas.json()['captcha_image']#取得验证码的base64编码 另一键：captcha_hash
    #【上面注意json转字典.json()】
    #print(tokenImg64Code)
    #data:image/jpeg;base64,/9j/4AAQ......
    #testBase64 = '/9j/4AAQSkZJRg......'
    #【注意：试存静态编码转base64可知 上面base64编码要split一下，逗号后面是】
    tokenImg64Code = tokenImg64Code.split(',')[1]#索引是从左向右0，1，2这样的注意
    #print(tokenImg64Code)
    tokenImg = base64.b64decode(tokenImg64Code)#转成图片存到本地
    with open(r'token.jpg','wb+') as fw:
        fw.write(tokenImg)

    #==取验证码，取完图片验证码
    # 根据本地图片输入，传到下面取手机验证码（比没图片验证码时多了一步，原理是一样的）=
    urlToken = 'https://h5.ele.me/restapi/eus/login/mobile_send_code'
    tokenImgValue = input('请输入图片验证码，图片见本机已下载：')
    dataToken = {
        "captcha_hash":"",
        "captcha_value":tokenImgValue,
        "mobile":tel,
        "scf":"ms"
    }
    tokenTel = sessionNew.post(urlToken,headers=headers,data=dataToken)#只有一键validate_token
    validateToken = tokenTel.json()['validate_token']
    #验证码传入登录请求
    validateCode = input('请输入手机验证码：')
    #手机输入验证码，传入登录请求
    #上面手机验证的validateToken validateCode两个一起传入登录请求中
    #==登录==
    urlLogin = 'https://h5.ele.me/restapi/eus/login/login_by_mobile'
    #登录请求是怎么找到的？页面正常登录勾选network里Preserve log,完成登录后即可找到。Preserve log可保障不会登录后跳走消息这个请求

    dataLogin = {
        "mobile":tel,
        "scf":"ms",
        "validate_code":validateCode,
        "validate_token":validateToken
    }

    resLogin = sessionNew.post(urlLogin,headers=headers,data=dataLogin)
    print(resLogin.status_code)
    if resLogin.status_code == 200:
        print('登录成功')
        #把cookie存到本地，下次查找时先从本地取cookie取不到再登录，随时更新session会话的cookie
        cookiesDict = req.utils.dict_from_cookiejar(resLogin.cookies)#解压
        cookiesStr = json.dumps(cookiesDict)#dumps json转字会串
        with open(r'cookiesFood.txt','a') as fwCookie:
            fwCookie.write(cookiesStr)
        
    else:
        print('登录失败，请检查')

#==读本地cookiesFood文件==
def readCookiesFoodFn():
    with open(r'cookiesFood.txt','r') as frCookie:
        cookieStr = frCookie.read()
        cookieDict = json.loads(cookieStr)#loads 字符串转json
        cookiejar = req.utils.cookiejar_from_dict(cookieDict)

        #sessionNew.cookies = cookiejar#更新会话cookies
        return (cookiejar)#本函数取到cookies即可，更新工作留在取用时进行
        


#找吃的
def findFoodFn():
    urlAddr = 'https://www.ele.me/restapi/v2/pois'
    myAddr = input('请输入你的送餐地址：')
    dataParams = {
        'extras[]': 'count',
        'geohash': 'wx4g0bmjetr7',
        'keyword': myAddr,
        'limit': '20',
        'type': 'nearby'
    }

    resAddr = sessionNew.get(urlAddr,headers=headers, params = dataParams)
    if resAddr.status_code == 200:#请求成功，则进行
        addrData = resAddr.json()[0]
        geohash = addrData['geohash']#注意前面取字典值，不能用.，和json不一样，别记混了
        latitude = addrData['latitude']
        longitude = addrData['longitude']
        urlRestaurants = 'https://www.ele.me/restapi/shopping/restaurants'
        dataParamsRest = {
            'extras[]': 'activities',
            'geohash': geohash,
            'latitude': latitude,
            'limit': '24',
            'longitude': longitude,
            'offset': '0',
            'terminal': 'web'
        }
        #==找餐馆==
        resFoods = sessionNew.get(urlRestaurants,headers=headers,params = dataParamsRest)
        if resFoods.status_code == 200:#请求成功
            #print(resFoods.json())
            foodDatas = resFoods.json()
            print("===="+addrData['name']+"附近的餐馆====")
            n = 0
            for item in foodDatas:
                n = n+1
                name = item['name']
                foodAddr = item['address']
                rate = item['rating']
                print("(%s)" % n)
                print(name+'\n'+foodAddr+'\n'+str(rate)+'\n-------------------')
        else:
            print('请求失败，请检查')
    else:#否则重新登录（【此处应精确换成未登录错误码】）
        loginFn()
        sessionNew.cookies = readCookiesFoodFn()#读本地cookies #更新到会话cookies

#读本地cookies
try:
    localCookies = readCookiesFoodFn()#读本地cookies
    sessionNew.cookies = localCookies#更新到会话cookies
except FileNotFoundError:#若没有，则登录
    loginFn()
    #更新最新会话cookies
    sessionNew.cookies = readCookiesFoodFn()#读本地cookies #更新到会话cookies

#==执行找吃的函数==
findFoodFn()