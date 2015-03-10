#!/usr/bin/python
# coding=utf-8

import cgi
import os
import sys
import Cookie
import hashlib
import json

import viewer
import dbconnector
import config
import cgitb
cgitb.enable()

SESSION_KEY = config.SESSION_KEY
DOCUMENT_ROOT = config.DOCUMENT_ROOT
header = 'Content-Type: text/html; charset=utf-8'
viewer = viewer.Viewer()
cookie = Cookie.SimpleCookie()
response = dict()
    
print(header)
res = 0;
params = {'site_url' : DOCUMENT_ROOT, 'reg' : '注册', 'reg_url' : 'reg', \
          'login' : '登录', 'login_url' : 'login', 'welcome' : '你好',\
          'img_path' : 'default.jpg'}

if ('REQUEST_METHOD' in os.environ and os.environ['REQUEST_METHOD'] == 'GET'):
    res = 1
else:    
    form = cgi.FieldStorage()
    username = cgi.escape(form.getfirst('user_name'))
    passwd = form.getfirst('password')
    
    db = dbconnector.DbConnector()
    try:
        rows = db.query("select * from users where UserName=%s", [username])
        if len(rows) == 0 or len(rows) > 1:
            res = -2
            response['msg'] = '该用户不存在'
        else:    
            md5 = hashlib.md5()
            md5.update(passwd)
            md5.update(rows[0]['Salt'])
            hash_passwd = md5.hexdigest()
            if hash_passwd != rows[0]['Password']:
                res = -3
                response['msg'] = '密码错误'
            else:
                cookie['session'] = rows[0]['SessionId']  
                cookie['session']['expires'] = 30 * 60
                cookie['user_name'] = username
                cookie['user_id'] = rows[0]['id']           
    except Exception, e:
        print(e)
    finally:
        db.close()
    

print cookie
print '\n'
response['code'] = res
if res == 1:
    viewer.load('header', params)
    viewer.load('login', params)
else:
    print json.dumps(response)
