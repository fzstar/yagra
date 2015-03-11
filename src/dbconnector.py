#!/usr/bin/python
# coding=utf-8

import hashlib
import time
import datetime
import MySQLdb as mysql
import config

class DbConnector(object):
    DB_USER = config.DB_USER
    DB_PASSWD = config.DB_PASSWD
    DB_HOST = config.DB_HOST
    DB_SOCKET = config.DB_SOCKET
    conn = None
    cursor = None
    
    def __init__(self):
        self.conn = mysql.connect(host=self.DB_HOST, user=self.DB_USER, passwd=self.DB_PASSWD,\
                             db="yagra", charset="utf8", unix_socket=self.DB_SOCKET)
    def execute(self, sql, params):
        for item in params:
            if type(item) == str:
                item = mysql.escape_string(item)
        self.cursor = self.conn.cursor(cursorclass = mysql.cursors.DictCursor)
        self.cursor.execute(sql,params)
        ret = self.conn.insert_id()
        self.conn.commit()
        if self.cursor != None:
            self.cursor.close()
        return int(ret)
    
    def query(self, sql, params):
        for item in params:
            if type(item) == str:
                item = mysql.escape_string(item)
        self.cursor = self.conn.cursor(cursorclass = mysql.cursors.DictCursor)
        self.cursor.execute(sql,params)
        ret = self.cursor.fetchall()
        if self.cursor != None:
            self.cursor.close()
        return ret

    def count(self, sql, params):
        for item in params:
            if type(item) == str:
                item = mysql.escape_string(item)
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
        print db.query("select * from users where id=%s", [7])
    except Exception, e:
        print("database error", e)
    finally:
        db.close()
