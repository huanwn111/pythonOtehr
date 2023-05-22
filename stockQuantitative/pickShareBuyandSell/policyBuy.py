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

    
#==取第一支大阳柱==
def getFirstSun(tblCols):

    #定义排序查询条件：trade_date asc 升序查询速度比降序快，与数据库默认升序一致
    #【注意：此处定义排序不可改动！因要计算前一天成交量vol，实现方法是按照升序排列取前一列】
    orders = "ts_code asc, trade_date asc"
    wheres = "1=1"
    datas = common.getDatasFromDb(tblName,startDateFirstSun,endDateFirstSun,wheres,orders)#从数据库初读数据
    #print(datas)#打印元组数据
    print("===开始计算大阳柱====")
    #取第一支大阳柱信息
    firstSunCode,firstSunOther,writeMark = getFirstSunFromCsv()

    nf = 0
    sunDatas = []#初查大阳柱列表（第一支，未去重）
    for i in range(len(datas)):
        if (i-1) > -1:
            #【==注意！：=======
            # 以下数据以数据元组序号为编号，数据库相关表字段结构变化时，此处要同步修改！==】
            if datas[i][0] == datas[i-1][0]:#相邻两行ts_code相同（为同一支股票）时才计算
                #==计算大阳柱==
                close = datas[i][5]#当日收盘价
                pre_close = datas[i][6]#前日收盘价
                vol = datas[i][9]#当日成交量
                pre_vol = datas[i-1][9]#前日成交量(时间是升序排列，i-1是前一天（时间更小）)
                
                #大阳柱条件
                sunCriteraion = (close - pre_close)/pre_close >= 0.04 and vol/pre_vol >1.9
                
                if sunCriteraion and datas[i][0] not in firstSunCode:#满足大阳条件，且ts_code不在第一支大阳柱列表中
                    trade_date_this_i = datas[i][1]#遍历的本条交易日期
                    #清除掉淘汰日期之前的第一支大阳柱（时间可=淘汰日期），filterFirstDict 过滤条件字典
                    if datas[i][0] in filterFirstDict.keys():#本条code如在过滤条件字典里，则
                        #打印过滤code和日期
                        delCode = datas[i][0]
                        delDate = filterFirstDict[datas[i][0]]#code和date已在字典中对应起来，通过code取对应的date，不用遍历判断取，字典很方便
                        print("===淘汰日股票编号和日期,淘汰日期：", delCode, delDate)

                        #遍历取交易日期>=淘汰日之后的记录用于收入大阳1号池
                        if trade_date_this_i >= delDate:

                            #符合条件的大阳柱加入初查列表
                            sunDatas.append(datas[i])
                            
                            print(nf,")")
                            print("==大阳柱==",datas[i])
                            print("前一天成交量：",datas[i-1][10])
                            print("前一天全记录：",datas[i-1])
                            print("--------------------") 
                            #从0条开始打印，与下面dataFrame 默认序号一致
                            nf = nf +1  
                    else:#无需淘汰删除时正常追加
                        #符合条件的大阳柱加入初查列表
                        sunDatas.append(datas[i])
                        
                        print(nf,")")
                        print("==大阳柱==",datas[i])
                        print("前一天成交量：",datas[i-1][10])
                        print("前一天全记录：",datas[i-1])
                        print("--------------------") 
                        #从0条开始打印，与下面dataFrame 默认序号一致
                        nf = nf +1


                    
        else:
            print(datas[i][0],",",datas[i][1],"是本时间段最前一条数据，前一天成交量取不到，或在上一个时间段已计算")

    #处理第一支大阳柱数据：去重；写入csv
    if len(sunDatas) >0 :
        #print("=========未去重的第一支大阳柱 元组格式=========")
        #print(sunDatas)
        #未去重大阳柱列表 元组格式转dataFrame格式
        sunDatasFrm = pd.DataFrame(list(sunDatas),columns=tblCols)
        #print("======去重前 dataFrame格式=======")
        #print(sunDatasFrm)

        #去重-得到第一支大阳柱
        sunDatasFrm.drop_duplicates('ts_code', keep='first', inplace=True)#按ts_code去重，保留首次出现的那条(因时间升序排，所以是时间小的,inplace=True替换原有dataFrame)
        print("======去重后 dataFrame格式=======")
        print(sunDatasFrm)
    
        #第一支大阳柱信息写入txt文件,文件路径在conf.py文件修改
        print("=====写入标记 是否初次=======",writeMark)
        try:
            if writeMark == 0:#第一次写入，覆盖，带列名
                sunDatasFrm.to_csv(firstSunPath, mode='w', index=False, columns = tblCols, encoding='utf-8')#第一次写入（1号股池文档为空时）不要追加a
            else:#非第一次写入，追加，不带列名
                sunDatasFrm.to_csv(firstSunPath, mode='a', index=False, columns = tblCols, header=False, encoding='utf-8')#1号股池有内容时，模式改为a，新的大阳柱追加a到后面。追加时不追加列标，注意：设置方法：header = False,columns要和第一次一样，不能设成false，否则写入失败
            print("第一支大阳柱已保存到",firstSunPath,"请查阅!~~")
        except:
            print("文件可能被占用，请关闭")
    else:
        print("此区间未查到大阳柱")

#==读取2号股池（csv文件） 第二支大阳柱信息==
def getSecondSunFromCsv():
    #定义第二支大阳柱ts_code列表
    secondSunCodeList = []
    writeMark_2 = 0
    try:
        datasCsv = pd.read_csv(secondSunPath, dtype = dtypes, encoding='utf-8')
        if len(datasCsv.values) > 0 :
            for item in datasCsv.values:
                ts_code_i = item[0]#ts_code
                trade_date_i = item[1]#第二支大阳柱的交易时间
                secondSunCodeList.append(ts_code_i)#存入第二支大阳柱ts_code列表
                writeMark_2 = 1#非第一次写入
        else:
            writeMark_2 = 0
        
    except:
        print("读2号股池路径不存在，或文件为空")
    return secondSunCodeList,writeMark_2
    

#==取第二支大阳柱==
def getSecondSun(daysGap,tblCols,tblCols2):

    #遍历取第一支大阳柱信息
    firstSunCodeList,firstSunOtherInfo,writeMark = getFirstSunFromCsv()
    #遍历取第二支大阳柱信息
    secondSunCodeList, writeMark_2 = getSecondSunFromCsv()
    sunDatasSd_1 = []#第二支大阳柱优股
    sunDatasSd_2 = []#第二支大阳柱良股

    for item in firstSunOtherInfo:
        firstSunCode = item[0]#第一支大阳柱ts_code
        firstSunStartDate = item[1]#第一支大阳柱trade_date
        firstSunPreClose = item[2]#第一支大阳柱pre_close
        print("\n===第一支大阳柱",firstSunCode,firstSunStartDate,"前日收盘价pre_close：",firstSunPreClose) 
        #查询起时
        startDateSecondSun = firstSunStartDate#第二支大阳柱的起查时间与第一支的trade_date一致，避免遗漏和多查数据，方便后面计算
        todayDate = datetime.datetime.now()
        gapDate = datetime.datetime.strptime(startDateSecondSun,'%Y-%m-%d') + datetime.timedelta(days=daysGap)
        #datetime.strptime字符串转日期格式，间隔daysGap天后
        #查询止时
        endDateSecondSun = todayDate if gapDate > todayDate else gapDate #python的三元运算符：真结果 if else条件 假结果
    
        #=从数据库初读数据=
        #定义排序查询条件：trade_date asc 升序查询速度比降序快，与数据库默认升序一致
        #【注意：此处定义排序不可改动！因要计算前一天成交量vol，实现方法是按照升序排列取前一列】
        orders = "ts_code asc, trade_date asc"
        if len(secondSunCodeList) > 0 :
            wheres = "ts_code = '" + firstSunCode + "' and ts_code not in " + str(tuple(secondSunCodeList)) #排除2号股池里已有的ts_code不查,第1号股池中上次查过的没在2号股池里的还会被重新查一遍避免遗漏
        else:
            wheres = "ts_code = '" + firstSunCode + "'"
        datas = common.getDatasFromDb(tblName,startDateSecondSun,endDateSecondSun,wheres,orders)

        if len(datas) > 0 :

            #print(datas)#打印从数据库初查的元组数据
            nS = 0#记录第二支大阳柱初查编号
            nsMarkOk = 0#记录一二支大阳柱之间数据满足筛选条件（close>第一支pre_close）的个数
            nsMarkAll = 0#记录第一二支大阳柱之间总数据条目
        
            #开始计算大阳柱
            for i in range(len(datas)):

                if (i-1) > -1:
                    #==计算大阳柱==
                    close = datas[i][5]#当日收盘价
                    pre_close = datas[i][6]#前日收盘价
                    vol = datas[i][9]#当日成交量
                    pre_vol = datas[i-1][9]#前日成交量(时间是升序排列，i-1是前一天（时间更小）)

                    #【==第二支大阳柱筛选条件：==
                    # ==第一二支之间（第二支若同时满足为最优，做标记）的股票收盘价close始终>=第一支的pre_close===】
                    #总数据条目+1
                    nsMarkAll = nsMarkAll + 1 
                    #遇到满足筛选条件的，筛选条件计数器+1 
                    if close >= firstSunPreClose:
                        nsMarkOk = nsMarkOk + 1 
                    
                    print("===第 (",i,") 条记录收盘价close：",close)
                    
                    #==淘汰1、2号大阳池中已有大阳柱，记录淘汰编号和日期到过滤条件字典（用于再次查第一支时过滤掉淘汰日之前的大阳柱）==
                    if close < firstSunPreClose:#当遇到收盘价低于第一支大阳前日收盘价时满足淘汰条件

                        #==处理1号池==
                        #删除满足条件的本ts_code所在行
                        delFirstSunFromCsv(datas[i][0],tblCols)#datas[i][0] 本条ts_code

                        #==处理2号池==
                        #删除满足条件的本ts_code所在行
                        delSecondSunFromCsv(datas[i][0],tblCols2)

                        #==记录本条ts_code和trade_date，用于取新第一支大阳时的过滤条件==
                        filterFirstDict[datas[i][0]] = datas[i][1]


                    #大阳柱条件
                    sunCriteraion = (close - pre_close)/pre_close >= 0.04 and vol/pre_vol >1.9
                    
                    if sunCriteraion:#满足大阳条件
                        #==先淘汰2号池中淘汰日之前的数据==
                        trade_date_this_i = datas[i][1]#遍历的本条交易日期
                        #清除掉淘汰日期之前的第一支大阳柱（时间可=淘汰日期），filterFirstDict 过滤条件字典
                        if datas[i][0] in filterFirstDict.keys():#本条code如在过滤条件字典里，则
                            #打印过滤code和日期
                            delCode = datas[i][0]
                            delDate = filterFirstDict[datas[i][0]]#code和date已在字典中对应起来，通过code取对应的date，不用遍历判断取，字典很方便
                            print("===淘汰日股票编号和日期,淘汰日期：", delCode, delDate)

                            #遍历取交易日期>=淘汰日之后的记录用于收入大阳2号池
                            if trade_date_this_i >= delDate:
                                print("====nsMarkOk:一二支大阳柱之间满足筛选条件的记录数:",nsMarkOk)
                                print("====nsMarkAll:一二支大阳柱之间总记录数:",nsMarkAll)

                                #一二支之间数据全部满足筛查条件
                                if nsMarkOk >= nsMarkAll:
                                    #符合条件的大阳柱加入初查列表
                                    sunDatasSd_1.append(datas[i])
                                    print("====优股：")
                                    print(nS,")")
                                    print("==第二支大阳柱==",datas[i])
                                    print("--------------------\n") 
                                #第二支大阳柱不满足close>第一支pre_close也可(此时满足nsMarkAll-nsMarkOk == 1 除去第二支最后一条记录其余数据都满足)，标记良股
                                if datas[i][5] < firstSunPreClose and nsMarkAll-nsMarkOk == 1:
                                    sunDatasSd_2.append(datas[i])
                                    print("====良股：")
                                    print(nS,")")
                                    print("==第二支大阳柱==",datas[i])
                                    print("--------------------\n") 
                                #删除大阳1号股池中有第二支大阳柱的记录
                                #delFirstSunFromCsv(datas[i][0],tblCols)#datas[i][0] 本条ts_code
                                #记录本条ts_code和trade_date，用于取新第一支大阳时的过滤条件
                                #filterFirstList.append([datas[i][0],datas[i][1]])
                                #从0条开始打印，与下面dataFrame 默认序号一致
                                nS = nS +1 

                        else:#无需淘汰删除时正常追加
                            print("====nsMarkOk:一二支大阳柱之间满足筛选条件的记录数:",nsMarkOk)
                            print("====nsMarkAll:一二支大阳柱之间总记录数:",nsMarkAll)

                            #一二支之间数据全部满足筛查条件
                            if nsMarkOk >= nsMarkAll:
                                #符合条件的大阳柱加入初查列表
                                sunDatasSd_1.append(datas[i])
                                print("====优股：")
                                print(nS,")")
                                print("==第二支大阳柱==",datas[i])
                                print("--------------------\n") 
                            #第二支大阳柱不满足close>第一支pre_close也可(此时满足nsMarkAll-nsMarkOk == 1 除去第二支最后一条记录其余数据都满足)，标记良股
                            if datas[i][5] < firstSunPreClose and nsMarkAll-nsMarkOk == 1:
                                sunDatasSd_2.append(datas[i])
                                print("====良股：")
                                print(nS,")")
                                print("==第二支大阳柱==",datas[i])
                                print("--------------------\n") 
                            #删除大阳1号股池中有第二支大阳柱的记录
                            #delFirstSunFromCsv(datas[i][0],tblCols)#datas[i][0] 本条ts_code
                            #记录本条ts_code和trade_date，用于取新第一支大阳时的过滤条件
                            #filterFirstList.append([datas[i][0],datas[i][1]])
                            #从0条开始打印，与下面dataFrame 默认序号一致
                            nS = nS +1 

                else:
                    print(datas[i][0],",",datas[i][1],"是本时间段最前一条数据，前一天成交量取不到，或在上一个时间段已计算")
            
            if nS <= 0:
                print("此区间没查到第二支大阳柱\n") 

        else:
            print("没查到数据")

    #处理第二支大阳柱优、良股数据：去重，写入csv
    #print("====第二支大阳柱优股列表 元组格式=====")
    #print(sunDatasSd_1)#第二支大阳柱优股列表 元组格式
    #print("====第二支大阳柱良股列表 元组格式=====")
    #print(sunDatasSd_2)#第二支大阳柱良股列表 元组格式
    #转为dataFrame格式，用pandas库函数去重，保留时间最接近的，即升序排的时间首次出现的

    #优股去重
    sunDatasSdFrm_1 = pd.DataFrame(list(sunDatasSd_1),columns = tblCols)
    sunDatasSdFrm_1.drop_duplicates('ts_code', keep='first', inplace=True)#第二支大阳柱去重
    sunDatasSdFrm_1['mark'] = 'A'#加优标记
    
    #良股去重
    sunDatasSdFrm_2 = pd.DataFrame(list(sunDatasSd_2),columns = tblCols)
    sunDatasSdFrm_2.drop_duplicates('ts_code', keep='first', inplace=True)#第二支大阳柱去重
    sunDatasSdFrm_2['mark'] = 'B'#加优良标记

    #合并优良股
    concatSunDatasSdFrm = pd.concat([sunDatasSdFrm_1,sunDatasSdFrm_2],axis=0,ignore_index=True)#ignore_index = True 重置索引

    if len(concatSunDatasSdFrm) > 0:
        if writeMark_2 == 0:#初次写入，覆盖，带列名
            #写入csv文件
            concatSunDatasSdFrm.to_csv(secondSunPath, mode='w', index=False, columns = tblCols2, encoding='utf-8')
        else:#非初次写入,追加，不带列名
            #写入csv文件
            concatSunDatasSdFrm.to_csv(secondSunPath, mode='a', index=False, columns = tblCols2, header = False, encoding='utf-8')
        print("====选定的第二支大阳柱优良股dataFrame=====")
        print(concatSunDatasSdFrm)
        print("选中的优良股第二支大阳柱已保存到",secondSunPath,"请查阅!~~")
    else:
        print("此区间没查到符合条件的第二支大阳柱")





#===============函数执行入口===================
""" 
if __name__ == '__main__':#加本句表示以下执行只在本页运行。当本.py文件被其它模块引用时以下不执行。

    #==取第一支大阳柱投入1号股池==
    getFirstSun(tblCols)

    #==第第二支大阳柱==
    getSecondSun(daysGap,tblCols,tblCols2)
 """
#【注意：在主入口文件中引用执行以下需从入口语句提出去】
#==取第一支大阳柱投入1号股池==
getFirstSun(tblCols)

#==第第二支大阳柱==
getSecondSun(daysGap,tblCols,tblCols2)