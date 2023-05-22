# -*- coding: utf-8 -*-
#===配置信息模块===

#==取第一支大阳柱相关配置信息==
#数据表
tblName = 'stock_daily'
# 起止时间（用于手动选择某时间段内的大阳柱）
startDateFirstSun = '2018-8-1'
endDateFirstSun = '2019-1-13'
#【注意：下次修改时间要和本次时间保持连续(即，下次开始时间=本次结束时间)，以免漏掉中间的大阳柱】

firstSunPath = 'G:\\firstSun.csv'


#==第二支大阳柱配置信息===
daysGap = 10 #设置第一支大阳柱往后的监测区间（例如：找出5天内的第二支大阳柱）,时间需整型

secondSunPath = 'G:\\secondSun.csv'

#==买入股票配置==
buyInfoTuple=(
    ("000014.SZ","2018/1/8"),
    ("000982.SZ","2018/1/4"),
    ("002147.SZ","2018/1/8"),
    ("002932.SZ","2018/7/20"),
)
#注意以上元组数据格式：
    # 整体一对圆括号；
    # 一条股票信息一组圆括号，ts_code在前，trade_date在后，用引号(单双均可)包围，逗号分开；
    # 日期格式：年/月/日 或 年-月-日，中间用/ 或 英文输入法下-短中线间隔均可；
    # 每条股票信息之间有逗号间隔，最末条逗号可有可无；

#卖股池地址
#text文件
sellHalfPath = 'G:\\sellHalf.text'
sellAllPath = 'G:\\sellAll.text'
#csv文件
sellHalfPathCsv = 'G:\\sellHalfCsv.csv'
sellAllPathCsv = 'G:\\sellAllCsv.csv'

