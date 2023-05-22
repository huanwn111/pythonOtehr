import pandas as pd
import datetime
import json
from django.http import HttpResponse

#==测试写入txt文件==
sellListHalf_text = [['000014.SZ',',', '2018-01-10','\n'], ['000014.SZ', ',','2018-01-11','\n']]
with open('G:\\testttt.txt','w+',encoding='utf-8') as f_w_half:
    for item in sellListHalf_text:
        f_w_half.writelines(item)
         

""" #===测试字典追加记录===
filterFirstDict = {}
for i in range(10):
    filterFirstDict['dict_'+str(i)] = i
print(filterFirstDict)
#结果：
#{'dict_0': 0, 'dict_1': 1, 'dict_2': 2, 'dict_3': 3, 'dict_4': 4, 'dict_5': 5, 'dict_6': 6, 'dict_7': 7, 'dict_8': 8, 'dict_9': 9}
filterFirstDict['dict_0'] = '新0'
print(filterFirstDict)#已有的键名会改掉之前的，没有的会新增
print(filterFirstDict['dict_0'])
#==判断是否存在某键名===
#if 'dict_1' in filterFirstDict:#判断字符串是否在字典中
if 'dict_1' in filterFirstDict.keys():#或精确一点判断字符串是否在字典的键中
    print("字典中有dict_1")
else:
    print("字典中无dict_1")
#===判断是否存在某值===
if 2 in filterFirstDict.values():
    print("字典值中有 2")
else:
    print("字典值中无 2")
 """
#=======测试dataFrame========

""" def test(request):
    return HttpResponse('你好！～')
    #return HTTPResponse(json.dumps({"name": "阿旺"}))
 """


#===测试dataFrame转json,前端网页显示====

#==读取2号股池（csv文件） 第二支大阳柱信息==
""" def getSecondSunFromCsv():
    #定义第二支大阳柱ts_code列表
    secondSunCodeList = []
    #jsonDatas ={}
    try:
        datasCsv = pd.read_csv('G:\\secondSun.csv', encoding='utf-8')
        for item in datasCsv.values:
            ts_code_i = item[0]#ts_code
            pre_close_i = item[6]#pre_close
            secondSunCodeList.append([ts_code_i,pre_close_i])#存入第二支大阳柱ts_code列表
        jsonDatas = datasCsv.to_json(orient='index')
    except:
        print("读2号股池路径不存在，或文件为空")
    return secondSunCodeList,jsonDatas
secondSunCodeList,jsonDatas = getSecondSunFromCsv()
print(secondSunCodeList)
 """

""" if __name__ == '__main__':
    secondSunCodeList,jsonDatas = getSecondSunFromCsv()
    print(jsonDatas) """


""" #===测试时间===
print(datetime.datetime.now().strftime('%Y%m%d'))#strftime日期转成字符串 2019-01-08 16:30:04.490026 变 20190108
print(datetime.datetime.strptime("2018-10-9",'%Y-%m-%d') + datetime.timedelta(days=5))#strptime字符串转成时间
print( datetime.datetime.strptime("2018-10-9",'%Y-%m-%d') + datetime.timedelta(days=5) > datetime.datetime.now())#日期加减比较，字符串需转成日期格式先
#x = 1 > 4?'错':'对'
#python中的三元运算符
#真结果 if else条件 假结果
x = "对" if 4>1 else "错"
print(x)
#结果
#20190108
#2018-10-14 00:00:00
#False """

pre_vol = [
    ('600.SH', "2000-10-9",1, 1, 1, 1, 1, 1, 1, 1, 1),
    ('603895.SH', "2018-10-9",3, 9.82, 9.22, 9.75, 1, 0.47, 5.0647, 111.0, 1422150.0),
    ('603895.SH', "2018-10-8",10, 9.82, 10.22, 9.75, 20, 0.47, 5.0647, 222.0, 123188.0),
    ('403894.SH', "2018-10-9",5, 9.82, 9.22, 9.75, 30, 0.47, 5.0647, 333.0, 323188.0),
    ('303893.SH', "2018-10-7",10, 9.82, 9.22, 9.75, 10, 0.47, 5.0647, 444.0, 523188.0),
    ('001', "2018-11-7",10, 1, 9.22, 9.75, 10, 0.47, 5.0647, 444.0, 523188.0),
    ('001', "2018-10-6",5, 1, 9.22, 9.75, 10, 0.47, 5.0647, 444.0, 523188.0),
    ('001', "2018-10-5",10, 9.82, 9.22, 9.75, 10, 0.47, 5.0647, 444.0, 523188.0)
]

""" secondSunCodeList = ['000001.SZ','000002.SZ','000003.SZ']
print(tuple(secondSunCodeList)) """

""" try:
    datasCsv = pd.read_csv('G:\\firstSun.csv')
    print(len(datasCsv))
except:
    pass """

""" for i in pre_vol:
    print(pre_vol[i]) """
#filterFirstList = [['001','100'],['002'],[]]
datasFrm = pd.DataFrame(list(pre_vol),columns=['ts_code','trade_date','open','high','low','close','pre_close','change','pct_change','vol','amount'])#将元组格式转为dataFrame
datasFrm.sort_values(['ts_code','trade_date'],inplace=True, ascending=True)
#datasFrm['pre_vol'] = datasFrm['vol'].shift(1)#加一列pre_vol，值为vol前一天（前一行）值
#去重
#datasFrm.drop_duplicates('ts_code', keep='first', inplace=True)#按ts_code去重，保留首次出现的那条(因时间升序排，所以是时间小的,inplace=True替换原有dataFrame)
#print(datasFrm)
datasFrm['level'] = '优'

#=======测试某值是否在dataFrame的一列中======
""" if '601.SH' in datasFrm['ts_code'].values:
    print("数据表ts_code列有为001的值")
else:
    print("数据表ts_code列无为001的值") """

""" #删除ts_code为600.SH那一行
colV = '600.SH'
#newDatas2 = datasFrm[datasFrm['ts_code'].isin([colV]).apply(lambda x: not x)]#注意not前没有return
#print(newDatas2)
#过滤掉open < 6 的数据
#newDatas3 = datasFrm[datasFrm['open']>=6]
#print(newDatas3) """
""" #【======测试按两列条件删除某行=======
#过滤出来（保留了，没有删掉） ts_code 为001的 open > 6 的数据
newDatas4 = datasFrm[(datasFrm["ts_code"].isin(["001"])) & (datasFrm["open"] < 6)]
print(newDatas4)#过滤到得到001号下open<6的记录
print(newDatas4.index.tolist())#取得它的索引
#删除掉以上索引所在行。
newDatas5 = datasFrm.drop( index = newDatas4.index.tolist(), axis = 1)#【可以】
print(newDatas5)
#=======测试按两列条件删除某行 完===========】 """
#====测试pandas的.where()==
""" newDatas6 = datasFrm.where(datasFrm["ts_code"].isin(["001"]))[datasFrm["open"] > 6]
print(newDatas6)#这样001倒是过滤出来了，其它行空值 """
#=====测试mask?=====

#==测试写入带列标题===
""" newDatas2.to_csv('G:\\testtest.csv', mode='w+', index = None, columns = ['ts_code','trade_date','open','high','low','close','pre_close','change','pct_change','vol','amount'])
rDatas = pd.read_csv('G:\\testtest.csv')
print(rDatas) """
""" groupSeries = datasFrm.groupby(['ts_code']).agg({'trade_date':min}).reset_index()

for row in groupSeries.values.tolist():
    print(row) """

""" groupFrm = datasFrm.groupby(['ts_code'])

for name, group in groupFrm:
    print(name)
    print(group) """




""" 
ts_codeList = []

for i in range(len(datas)):
    if datas.count(datas[i][0]) >1:
        print(datas[i][0])
    #if len(datas[i][0]) > 1:
    #    print([datas[i][0],datas[i][1]])
"""
#print(ts_codeList)
#===测试yield用法===
""" def testYield():
    n=0
    m = 1
    while n < 5:
        yield n,m
        #yield 相当于return，
        #不同是：返回可迭代循环使用的结果
        n = n + 1
        m = m *2

for i,j in testYield():
    print(i,j) """

""" #结果：
0 1
1 2
2 4
3 8
4 16 """