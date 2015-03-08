#!C:\Program Files\Python27\python.exe
# coding=utf-8

import cgi
import os
import viewer
import Cookie
import dbconnector

DOCUMENT_ROOT = '/cgi-bin/yagra'
header = 'Content-Type: text/html; charset=utf-8\n\n'
viewer = viewer.Viewer()

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
    
if ('REQUEST_METHOD' in os.environ and os.environ['REQUEST_METHOD'] == 'GET'):
    print(header)
    params = {'site_url' : DOCUMENT_ROOT, 'reg' : '注册', 'reg_url' : 'reg.py', \
              'login' : '登录', 'login_url' : 'login.py', 'welcome' : '你好'}
    session = get_session()
    if session != None:
        params['welcome'] = '你好 '+session['user_name'].value
        params['reg'] = session['user_name'].value
        params['reg_url'] = 'index.py'
        params['login'] = '注销'
        params['login_url'] = 'logout.py'
        
    viewer.load('header', params)
    viewer.load('index', params)

