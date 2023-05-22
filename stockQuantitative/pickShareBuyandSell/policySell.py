# -*- coding: utf-8 -*-
import common
from conf import tblName,buyInfoTuple,sellHalfPath,sellAllPath,sellHalfPathCsv,sellAllPathCsv
import pandas as pd
import datetime
from contextlib import contextmanager
tblCols = ['ts_code','trade_date','open','high','low','close','pre_close','change','pct_change','vol','amount']
 
#从数据库初查已买入股票

def findBuyStock():
    #遍历买入股编号、买入日期元组（元组操作类似list，效率更高）
    for i in range(len(buyInfoTuple)):

        ts_code_buy_i = buyInfoTuple[i][0]
        trade_date_buy_i = buyInfoTuple[i][1]
        print(ts_code_buy_i)
        print(trade_date_buy_i)

        startDateBuy = trade_date_buy_i#从数据库跟踪查询的初始日期
        endDateBuy = datetime.datetime.now().strftime("%Y-%m-%d")#从数据库跟踪查询的截止日期
        orders = "ts_code asc, trade_date asc"#【注意排序不能改，后面计算基于此】
        wheres = "ts_code = '" + ts_code_buy_i + "'"
        datasBuy = common.getDatasFromDb(tblName,startDateBuy,endDateBuy,wheres,orders)

        yield datasBuy


#计算处理从数据库中眼踪取到的数据
def sellCondition(tblCols):
    sellListHalf_text = []#卖一半存入记事本数据（编号与日期）整合
    sellListHalf_csv = []#卖一半存入csv文件数据（全信息）整合
    sellListAll_text = []#清仓存入记事本数据（编号与日期）整合
    sellListAll_csv = []#清仓存入csv文件数据（全信息）整合
    for datasBuyItem in findBuyStock():#取用findBuyStock() yield返回的可迭代结果
        #print(datasBuy)
        #print("========================\n\n")
        if datasBuyItem is not None:

            for item in datasBuyItem:#遍历跟踪买入股票记录

                pct_change_buy_i = item[8]#取数据列索引8涨幅 pct_change
                #【====条件一：卖一半=====】
                if pct_change_buy_i >= 4:#涨幅超过4（%数据取下来不带单位）这条记录取半位置
                    close_buy_hf = item[5]#数据列第5号收盘价 close
                    pre_close_buy_hf = item[6]#数据列第6号前日收盘价 pre_close
                    halfPos = (close_buy_hf + pre_close_buy_hf)/2# 二分之一位置定义：(这天收盘价+前日收盘价)/2
                    print("====",item[0],item[1],">4%涨涨那天的收盘价：",item[5],"半位置:",halfPos,"====")

                print("=====遍历的本条记录收盘价：",item[5],item[0],item[1],"=======\n")
                #本条记录收盘价
                close_buy_i = item[5]

                if close_buy_i < halfPos:#【==本条记录收盘价<半位值时取此条放入卖股1号池==】

                    #追加到text存储文件列表
                    sellListHalf_text.append([str(item[0]),',',str(item[1]),'\n'])
                    #追加到csv存储文件列表
                    sellListHalf_csv.append(item)
                    print("本条记录符合卖股条件一（需卖一半）：","收盘价：",close_buy_i,"\n全信息：",item,"\n")

                else:
                    print("本股次无需卖一半")

                #==【条件二：遇到收盘价<涨幅超4%那天的前日收盘价清仓】==
                if close_buy_i < pre_close_buy_hf:

                    #追加到text存储文件列表
                    sellListAll_text.append([str(item[0]),',',str(item[1]),'\n'])
                    #追加到csv存储文件列表
                    sellListAll_csv.append(item)
                    print("本条记录符合卖股条件二（需清仓）：","收盘价：",close_buy_i,"\n全信息：",item,"\n")

                else:
                    print("本股本次无需清仓")


    #==文件写入或发邮件区==
    #==卖一半
    #写入txt
    with open(sellHalfPath,'w+',encoding='utf-8') as f_w_half:
        for itemHalf in  sellListHalf_text:
            f_w_half.writelines(itemHalf) 
    #写入csv
    sellListHalf_csv_frm = pd.DataFrame(list(sellListHalf_csv), columns=tblCols)
    sellListHalf_csv_frm.to_csv(sellHalfPathCsv, mode='w+', encoding='utf-8', columns=tblCols, index = False)                

    #==清仓
    #写入txt
    with open(sellAllPath,'w+',encoding='utf-8') as f_w_half:
        for itemAll in sellListAll_text:
            f_w_half.writelines(itemAll) 
    #写入csv
    sellListAll_csv_frm = pd.DataFrame(list(sellListAll_csv), columns=tblCols)
    sellListAll_csv_frm.to_csv(sellAllPathCsv, mode='w+', encoding='utf-8', columns=tblCols, index = False)                

    #打印列表
    print("===卖一半txt==")
    print(sellListHalf_text)
    print("===卖一半csv==")
    print(sellListHalf_csv_frm)
    print("===清仓txt==")
    print(sellListAll_text)
    print("===清仓csv==")
    print(sellListAll_csv_frm)


if __name__ == "__main__":
    #在本页内执行卖策略
    sellCondition(tblCols)

    
