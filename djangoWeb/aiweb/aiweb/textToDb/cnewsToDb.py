#cnews.text新闻导入数据库
import pymysql

conn = pymysql.connect(host='localhost',user='root',password='',db='py_aiweb',port=3306)
print("数据连接完成")

cur = conn.cursor()

sqlAdd = 'insert into py_aiweb_cnews_tbl(className,content) values (%s,%s)'
#params = [['新2','新22222'],['新3','新333333'],['新4','新444']]
#executemany第二参静态测试
params = []
#读text文件
with open(r'G:\vscWorkspace\djangoWeb\aiweb\aiweb\textToDb\cnews.txt','r',encoding='utf-8') as f:
    fObj = f.readlines()
    for item in fObj:
        params.append(item.split('\t'))

#print(params) #打印看符合需求格式
try:
    cur.executemany(sqlAdd,params)
    print("批量添加完成")
finally:
    conn.commit()
    cur.close()
    conn.close()


