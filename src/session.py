#!C:\Program Files\Python27\python.exe
# coding=utf-8

import os
import Cookie
import hmac

import dbconnector

def get_session():
    if 'HTTP_COOKIE' in os.environ:
        cookie = Cookie.SimpleCookie(os.environ['HTTP_COOKIE'])
        session = cookie['session'].value
        db = dbconnector.DbConnector()
        sql = 'select * from users where UserName = %s AND SessionId = %s'
        param = [cookie['user_name'].value, session]
        rows = db.query(sql, param)
        if len(rows) == 1:
            return cookie
    return None
