from tushare_test.support import log
from tushare_test.support import databaseConnect

import pandas as pd

#import tushare as ts

stockLog = log.logInit("fileoutput") #log初始化

def get_relative_high_point(stock='000001.SZ', windows=10,length = 100):
    """
    获取某一只股票的相对高点
    :param stock:股票代码
    :param windows: 窗口时间
    :param length: 检索时间
    :return:
    """
    sql = "SELECT trade_date,high FROM stock.stock_daily where ts_code = '{}' order by trade_date".format(stock)

    relative_high_point = pd.DataFrame()

    with databaseConnect.pandas_mysql_read(sql=sql) as pd_mysql_df:
        row_count = min(pd_mysql_df.shape[0],length)
        for row in range (pd_mysql_df.shape[0]+1-row_count,pd_mysql_df.shape[0]+1):
            temp_df = pd_mysql_df.iloc[row-windows:row]
            max_row = temp_df['high'].idxmax()
            if max_row>row-windows and max_row<row-1:
                relative_high_point = relative_high_point.append(temp_df.loc[[max_row],])
    if len(relative_high_point) == 0:
        return relative_high_point
    else:
        return relative_high_point.drop_duplicates()

def get_relative_low_point(stock='000001.SZ', windows=10,length = 100):
    """
    获取某一只股票的相对高点
    :param stock:股票代码
    :param windows: 窗口时间
    :param length: 检索时间
    :return:
    """
    sql = "SELECT trade_date,low FROM stock.stock_daily where ts_code = '{}' order by trade_date".format(stock)

    relative_low_point = pd.DataFrame()

    with databaseConnect.pandas_mysql_read(sql=sql) as pd_mysql_df:
        row_count = min(pd_mysql_df.shape[0],length)
        for row in range (pd_mysql_df.shape[0]+1-row_count,pd_mysql_df.shape[0]+1):
            temp_df = pd_mysql_df.iloc[row-windows:row]
            min_row = temp_df['low'].idxmin()
            if min_row>row-windows and min_row<row-1:
                relative_low_point = relative_low_point.append(temp_df.loc[[min_row],])
    if len(relative_low_point) == 0:
        return relative_low_point
    else:
        return relative_low_point.drop_duplicates()

if __name__ == '__main__':
    print(get_relative_high_point(length=10))
    print(get_relative_low_point(length=10))
	
#===以下略===

#==买股模块==
# -*- coding: utf-8 -*-
#==股票买入策略模块（1）两支大阳柱 ==
import common
from conf import tblName,startDateFirstSun,endDateFirstSun,firstSunPath,secondSunPath,daysGap
import pandas as pd
import csv
import datetime
#stock_daily表字段
tblCols = ['ts_code','trade_date','open','high','low','close','pre_close','change','pct_change','vol','amount']
tblCols2 = ['ts_code','trade_date','open','high','low','close','pre_close','change','pct_change','vol','amount','mark']
dtypes = {'ts_code':str,'trade_date':str,'open':float,'high':float,'low':float,'close':float,'pre_close':float,'change':float,'pct_change':float,'vol':float,'amount':float}
filterFirstDict = {}#第1，2号大阳池淘汰过滤条件（遇到收盘价低于第1支大阳柱前日收盘价即删除1，2号池中本编号本日期的记录，且下次取新大阳柱时需排除掉淘汰日期之前的）

#==删除淘汰大阳1号池（第一支大阳柱）==
def delFirstSunFromCsv(ts_code_del,tblCols):
    try:
        #1号池源数据
        datasFirstSunRaw = pd.read_csv(firstSunPath, dtype = dtypes, encoding='utf-8')
        if ts_code_del in datasFirstSunRaw['ts_code'].values :#如果ts_code_del在大阳池中则删除满足淘汰条件的记录
            #删除指定行
            #datasFirstSunNew = datasFirstSunRaw[datasFirstSunRaw['ts_code'].isin([ts_code_del]).apply(lambda x : not x)]
            datasFirstSunNew = datasFirstSunRaw[datasFirstSunRaw['ts_code']!=ts_code_del]#过滤剩下不等于删除条件的
            #注意上面过滤条件，不用写编号与交易日结合条件，因为1号大阳池里只有一只大阳柱，且肯定在发生删除条件这天之前(发生在之后的删除掉后，下次还会收上来，且时间按从前往后查也不会出现有过滤条件之后的日期)
            #且第二只大阳柱之前如果有满足过滤条件的，也不会收到第2池里，即已经在第2池里的之前日期不会出现过滤条件，所以过滤条件肯定也是出现在它后面的日期，只传编号删除即可（2号池只有一个这个编号的股，且在过滤条件发生日期之前，日期条件自动满足）
            print("===过滤后的1号池数据行数：",datasFirstSunNew.shape[0])
            #新数据重新写入替换原大阳1号股池
            datasFirstSunNew.to_csv(firstSunPath, mode='w', index=None, columns=tblCols, encoding='utf-8')
        else:
            print("本次1号大阳池没有要淘汰的数据")
    except:
        print("读1号股池路径不存在，或文件为空")
#==删除淘汰大阳2号池（第二支大阳柱）==
def delSecondSunFromCsv(ts_code_del,tblCols2):
    try:
        #2号池源数据
        datasSecondSunRaw = pd.read_csv(secondSunPath, dtype = dtypes, encoding='utf-8')
        if ts_code_del in datasSecondSunRaw['ts_code'].values : #若源数据表中有要删的编号，则按条件删除
            #删除指定行
            #datasSecondSunNew = datasSecondSunRaw[datasSecondSunRaw['ts_code'].isin([ts_code_del]).apply(lambda x : not x)]
            datasSecondSunNew = datasSecondSunRaw[datasSecondSunRaw['ts_code']!=ts_code_del]#过滤剩下不等于删除条件的
			#注意上面过滤条件，不用写编号与交易日结合条件，因为1号大阳池里只有一只大阳柱，且肯定在发生删除条件这天之前(发生在之后的删除掉后，下次还会收上来，且时间按从前往后查也不会出现有过滤条件之后的日期)
            #且第二只大阳柱之前如果有满足过滤条件的，也不会收到第2池里，即已经在第2池里的之前日期不会出现过滤条件，所以过滤条件肯定也是出现在它后面的日期，只传编号删除即可（2号池只有一个这个编号的股，且在过滤条件发生日期之前，日期条件自动满足）。
            print("===过滤后的2号池数据行数：",datasSecondSunNew.shape[0])
            #删除后的数据写入2号股池
            datasSecondSunNew.to_csv(secondSunPath, mode='w', index=None, columns=tblCols2,encodin='utf-8')
        else:
            print("本次2号大阳池没有要淘汰的数据")
    except:
        print("读2号股池路径不存在，或文件为空")

#==读取1号股池（csv文件） 第一支大阳柱信息==
def getFirstSunFromCsv():
    #定义第一只大阳柱ts_code列表
    firstSunCodeList = []
    #定义第一只大阳柱其它信息列表
    firstSunOtherInfo = []
    writeMark = 0
    try:
        datasCsv = pd.read_csv(firstSunPath, dtype = dtypes, encoding='utf-8')
        if len(datasCsv.values) > 0:
            for item in datasCsv.values:
                ts_code_i = item[0]#ts_code
                trade_date_i = item[1]#时间
                pre_close_i = item[6]#前一天收盘价
                firstSunCodeList.append(ts_code_i)#存入第一支大阳柱ts_code列表
                firstSunOtherInfo.append([ts_code_i,trade_date_i,pre_close_i])

                writeMark =1 #第一次写入为0，非第一次写入为1
        else:
            writeMark = 0

        #return firstSunCodeList,firstSunOtherInfo,writeMark

    except:
        print("读1号股池路径不存在，或文件为空")
    return firstSunCodeList,firstSunOtherInfo,writeMark
	

	#=====以下略=====
	
	
	#==common.py==
	
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


		
