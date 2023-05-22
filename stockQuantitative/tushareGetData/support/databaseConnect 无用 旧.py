#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
# from sqlalchemy import create_engine

import contextlib

import pandas as pd

#mysql数据库连接
@contextlib.contextmanager
def mysql_operator(host='localhost', user='root', password='', db='sys', port=3306):
    conn = pymysql.connect(host = host,port = port,user = user,passwd = password,db = db)
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    finally:
        cursor.close()
        conn.close()

@contextlib.contextmanager
def pandas_mysql_read(sql,index_clo=None,host='localhost', user='root', password='', db='sys', port=3306):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db)
    df = pd.read_sql(sql, con=conn,index_col=index_clo)
    try:
        yield df
    finally:
        conn.close()

if __name__ == '__main__':
    with pandas_mysql_read(sql='select * from stock_basic', db='stock') as df:
        print(df)