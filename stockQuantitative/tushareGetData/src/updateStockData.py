#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=no-member
#上面一行解决vscode 中ts.pro_api()无此成员BUG pylint 的 *E1101* 错误
import pymysql
import time
import datetime

from support import log
from support import databaseConnect

import tushare as ts

stock_log = log.logInit("fileoutput")  # log初始化


def update_stock_data(api, stock_code):
    try:
        start_dt = '20180101'
        time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
        end_dt = time_temp.strftime('%Y%m%d')
        df = ts.pro_bar(pro_api=api, ts_code=stock_code, adj='qfq', start_date=start_dt, end_date=end_dt)  # 获取数据
        stock_data = df.where(df.notnull(), None)  # 将Nan转换为None

        # df = ts.pro_bar(pro_api=api, ts_code=stock_code, adj='qfq')  # 获取数据
        # stock_data = df.where(df.notnull(), None)  # 将Nan转换为None

        data_list = []

        for row in stock_data.itertuples(index=False, name=None):  # 将dataframe转换为list
            data_list.append(row)

        with databaseConnect.mysql_operator(db='stock') as cursor:
            cursor.execute("""select open,trade_date from stock.stock_daily where ts_code 
                                = %s order by trade_date desc""", (stock_code))    # 查询stock的最近的数据
            data = cursor.fetchone()
            if data is None:  # 插入所有数据
                cursor.executemany("""insert into stock.stock_daily 
                                (`ts_code`,`trade_date`,`open`,`high`,`low`,`close`,`pre_close`,`change`,`pct_change`,`vol`,`amount`) 
                                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", data_list)
                stock_log.info('{},插入所有数据'.format(stock_code))
            elif stock_data.loc[data[1].strftime('%Y%m%d'), 'open'] == data[0]:  # 插入所有数据
                update_row_count = stock_data.loc[:data[1].strftime('%Y%m%d')].shape[0] - 1
                if update_row_count != 0:
                    cursor.executemany("""insert into stock.stock_daily 
                                    (`ts_code`,`trade_date`,`open`,`high`,`low`,`close`,`pre_close`,`change`,`pct_change`,`vol`,`amount`) 
                                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                                       data_list[0:update_row_count])  # 插入所以数据
                    stock_log.info("{},插入{}行新数据".format(stock_code, update_row_count))
            else:  # 更新所有数据
                cursor.execute("delete from stock.stock_daily where ts_code = %s", (stock_code))   # 删除所有数据
                cursor.executemany("""insert into stock.stock_daily 
                                (`ts_code`,`trade_date`,`open`,`high`,`low`,`close`,`pre_close`,`change`,`pct_change`,`vol`,`amount`) 
                                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", data_list)   # 插入所有数据
                stock_log.info("{},更新所有数据".format(stock_code))
            print(stock_code)
    except pymysql.Error as e:
        stock_log.error(e)
    except:
        stock_log.error('other error')
    else:
        stock_log.info('finish update stock data')


if __name__ == '__main__':
    #c8c44b9ef173fa35b3a09aadb7cf4c2f0513c232f8a4c6ca608b81f1
    pro = ts.pro_api('c8c44b9ef173fa35b3a09aadb7cf4c2f0513c232f8a4c6ca608b81f1')
    update_stock_data(pro, '000001.SZ')
