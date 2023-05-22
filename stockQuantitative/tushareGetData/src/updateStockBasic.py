#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=no-member
#上面一行解决vscode 中ts.pro_api()无此成员BUG pylint 的 *E1101* 错误
import pymysql

from support import log
from support import databaseConnect

import tushare as ts


stock_log = log.logInit("fileoutput") #log初始化
def testFn(msg):
    return msg
def update_stock_base(pro):
    """
    更新股票代码清单
    :param pro: token
    :return: stock_List
    """
    try:
        stock_base_data = pro.stock_basic(list_status='L')
        with databaseConnect.mysql_operator(db='stock') as cursor:
            cursor.execute("""delete from stock.stock_basic""")
            stock_base_data_list = []
            for row in stock_base_data.itertuples(index=False,name=None):
                stock_base_data_list.append(row)
            cursor.executemany("""insert into stock.stock_basic (ts_code, symbol, name, area, industry, market, list_date) values(%s, %s, %s, %s, %s, %s, %s)""",stock_base_data_list)
            cursor.execute("""select ts_code from stock.stock_basic""")
            stockList = cursor.fetchall()
    except pymysql.Error as e:
        stock_log.error(e)
    except:
        stock_log.error('other error')
    else:
        stock_log.info('finish update stock basic')
        return stockList

def get_stock_base():
    """
    获取股票代码清单
    :return:
    """
    try:
        with databaseConnect.mysql_operator(db='stock') as cursor:
            cursor.execute("""select ts_code from stock.stock_basic""")
            stockList = cursor.fetchall()
    except pymysql.Error as e:
        stock_log.error(e)
    except:
        stock_log.error('other error')
    else:
        stock_log.info('finish update stock basic')
        return stockList

if __name__ == '__main__':
    #c8c44b9ef173fa35b3a09aadb7cf4c2f0513c232f8a4c6ca608b81f1
    pro = ts.pro_api('c8c44b9ef173fa35b3a09aadb7cf4c2f0513c232f8a4c6ca608b81f1')
    update_stock_base(pro)