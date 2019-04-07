import requests, json, time, random
print("\n你好，我是你的机器人小器，可以和我聊天了~~")
n = 0;
while n <= 5:
    
    mywords = input("\nQ:");
    userid = str(random.randint(1,100000000));#生成1到100000000之间的整数随机数
    apikey = 'a4500597c3bf4a41baf17d2a83767760';
#***===json.dumps把字典格式变json格式，字典并不直接等于json格式，虽然长一样，可能编码不同，注意===*** 
    datas = json.dumps({
        "perception":{
            "inputText":{
                "text":mywords
            }
        },
        "userInfo":{
            "apiKey":apikey,
            "userId":userid
        }
    })
    
    res = requests.post('http://openapi.tuling123.com/openapi/api/v2', datas)
    print("A:",json.loads(res.text)['results'][0]['values']['text']);
    
    n = n+1;
if n > 5:
    print("\nA: 我要休息了，明天见～\n")