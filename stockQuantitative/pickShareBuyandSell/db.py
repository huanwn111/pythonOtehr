# -*- coding: utf-8 -*-
#==数据库操作模块==

import pymysql
from contextlib import contextmanager

#连接数据库读数据
@contextmanager
def dbQuery(host='localhost',db='stock', user='root', passwd='', port=3306,charset='utf8'):
    print("==========连接数据库===========")
    conn = pymysql.connect(host=host, db=db, user=user, passwd=passwd, port=port,charset=charset)
    cur = conn.cursor()
    try:
        yield cur
        conn.commit()
    finally:
        cur.close()
        conn.close()


