# -*- coding: utf-8 -*-
#==公共函数模块==
import db

#==从数据库初取数据==
 #【查询参数说明：
    # startDate、endDate（起、止日期）在conf.py文件设置，用于手动选择某时间段的大阳柱
    # orders（排序条件）定制数据排列格式，用于后续计算前一条记录的vol成交量等
    # 注意:此处粗查不可加Group by 过滤筛选，防止遗漏数据。
    # tblName操作表名称，在conf.py文件设置】

def getDatasFromDb(tblName,startDate,endDate,wheres,orders):
    with db.dbQuery() as cur:
        sql = "select * from %s where trade_date between '%s' and '%s' and %s order by %s" % (tblName,startDate,endDate,wheres,orders)
        #print(sql)
        print("=====开始从数据库读数据=====")
        cur.execute(sql)
        rsDatas = cur.fetchall()#返回默认元组格式数据
        return rsDatas 

