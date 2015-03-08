#!C:\Program Files\Python27\python.exe
# coding=utf-8

import hashlib
import time
import datetime
import MySQLdb as mysql

class DbConnector(object):
    DB_USER = 'root'
    DB_PASSWD = ''
    DB_HOST = 'localhost'
    conn = None
    cursor = None
    
    def __init__(self):
        self.conn = mysql.connect(host=self.DB_HOST,user=self.DB_USER,passwd=self.DB_PASSWD,\
                             db="yagra",charset="utf8")

    def execute(self, sql, params):
        self.cursor = self.conn.cursor(cursorclass = mysql.cursors.DictCursor)
        ret = self.cursor.execute(sql,params)
        self.conn.commit()
        if self.cursor != None:
            self.cursor.close()
        return ret
    
    def query(self, sql, params):
        self.cursor = self.conn.cursor(cursorclass = mysql.cursors.DictCursor)
        self.cursor.execute(sql,params)
        ret = self.cursor.fetchall()
        if self.cursor != None:
            self.cursor.close()
        return ret

    def count(self, sql, params):
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql,params)
        ret = self.cursor.fetchone()[0]
        if self.cursor != None:
            self.cursor.close()
        return ret
    
    def close(self):
        if self.conn != None:
            self.conn.close()
    
        
if __name__ == '__main__':
    db = DbConnector()
    sql = "insert into users(UserName,Password,Salt) values (%s,%s,%s)"
    md5 = hashlib.md5()
    salt = str(time.mktime(datetime.datetime.now().timetuple()))
    md5.update("asdfghj")
    md5.update(salt)
    hash_passwd = md5.hexdigest()
    params = ["user1", hash_passwd, salt]
    
    try:
        print db.query("select * from users where UserName=%s", "user4")
    except Exception, e:
        print("database error", e)
    finally:
        db.close()
