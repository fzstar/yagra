#!/usr/bin/python
# coding=utf-8

import cgi
import os
import sys
import Cookie
import json

from hashutil import HashUtil
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
res = 0
params = {'site_url' : DOCUMENT_ROOT, 'reg' : '注册', 'reg_url' : 'reg', \
          'login' : '登录', 'login_url' : 'login', 'welcome' : '你好',\
          'img_path' : 'default.jpg'}

if ('REQUEST_METHOD' in os.environ and os.environ['REQUEST_METHOD'] == 'GET'):
    res = 1
else:
    form = cgi.FieldStorage()
    username = cgi.escape(form.getfirst('user_name'))
    passwd = form.getfirst('passwd')
    confirm_passwd = form.getfirst('confirm_passwd')
    if passwd != confirm_passwd:
        res = -2
        response['msg'] = '两次输入的密码不一致'
    else:    
        db = dbconnector.DbConnector()
        try:
            if (db.count("select count(*) from users where UserName=%s", [username]) > 0):
                res = -3
                response['msg'] = '用户名已存在'
            else:    
                sql = "insert into users(UserName,Password,SessionId,Token) values (%s,%s,%s,%s)"
                sid = HashUtil.get_session_id(username)
                token = HashUtil.get_md5(username)
                sql_params = [username, passwd, sid, token]
                user_id = db.execute(sql, sql_params)
                cookie['session'] = sid
                cookie['session']['expires'] = 30 * 60
                cookie['user_name'] = username
                cookie['user_id'] = user_id
                
        except Exception as e:
            print("error", e)
        finally:
            db.close()

print(cookie.output())
print '\n'
#viewer.load('header', params)
response['code'] = res
if res == 1:
    viewer.load('header', params)
    viewer.load('reg', params)
else:
    print(json.dumps(response))
#else:
    #viewer.set_redirect('index.py')
    #viewer.load('index', params)
