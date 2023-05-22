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