# -*- coding: utf-8 -*-

from UserInfo.settings import *
import pymysql
import sys

try:
    conn=pymysql.connect(
            user=MYSQL_USER,
                    passwd=MYSQL_PASSWORD,
                    host=MYSQL_HOST,
                    port=MYSQL_PORT,
                    database=MYSQL_DB,
                    charset=CHARSET)
    cur=conn.cursor()
except conn.Error as e:
    sys.exit('Spider Failed to connect database.',e)
    
try:
    cur.execute("select COLUMN_NAME from information_schema.COLUMNS where table_name='author_info'")
except Exception:
    sys.exit('have an error !!')
    
all_data=cur.fetchall()
for fc in all_data:
#   print("item['xxx']") 
   print("item['%s"% fc[0]+"']"+',')