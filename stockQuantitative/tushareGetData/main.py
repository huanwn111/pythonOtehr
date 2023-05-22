#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=no-member
#上面一行解决vscode 中ts.pro_api()无此成员BUG pylint 的 *E1101* 错误
import tushare as ts
import time

from src import updateStockBasic
from src import updateStockData


from multiprocessing.dummy import Pool
time.sleep(1)

if __name__ == '__main__':
    pool = Pool(2)
#旧c34877586f962f39f0c69de2a027c30fba8eb05bda5a1f9ae525449b
#新c8c44b9ef173fa35b3a09aadb7cf4c2f0513c232f8a4c6ca608b81f1
    pro = ts.pro_api('c8c44b9ef173fa35b3a09aadb7cf4c2f0513c232f8a4c6ca608b81f1')
    #print(updateStockBasic.testFn('123123'))
    stockList = updateStockBasic.update_stock_base(pro)        # 更新并获取stock清单
    #print(stockList)
    if stockList is not None:
        for stock_code in stockList:
            if __name__ == '__main__':
                updateStockData.update_stock_data(pro, stock_code[0])
            # pool.apply_async(updateStockData.update_stock_data, (pro,stock_code[0]),)
            # updateStockData.update_stock_data(pro,stock_code[0])
            
    pool.close()
    pool.join()


