#!/usr/bin/python
# coding=utf-8

import cgi
import os
import sys
import Cookie

from hashutil import HashUtil
import viewer
import dbconnector
import config
import cgitb
cgitb.enable()

SESSION_KEY = config.SESSION_KEY
DOCUMENT_ROOT = config.DOCUMENT_ROOT
viewer = viewer.Viewer()
cookie = Cookie.SimpleCookie()
response = dict()

res = 0
params = {'site_url': DOCUMENT_ROOT, 'reg': '注册', 'reg_url': 'reg',
          'login': '登录', 'login_url': 'login', 'welcome': '你好',
          'img_path': 'default.jpg'}

if ('REQUEST_METHOD' in os.environ and os.environ['REQUEST_METHOD'] == 'GET'):
    res = 1
else:
    form = cgi.FieldStorage()
    username = cgi.escape(form.getfirst('user_name'))
    token_passwd = form.getfirst('passwd')

    db = dbconnector.DbConnector()
    try:
        rows = db.query("select * from users where UserName=%s", [username])
        db.execute("update users set LoginToken='' where UserName=%s", [username])
        if len(rows) == 0 or len(rows) > 1:
            res = -2
            response['msg'] = '该用户不存在'
        else:
            save_token_passwd = HashUtil.get_md5(rows[0]['Password'], rows[0]['LoginToken'])
            if token_passwd != save_token_passwd:
                res = -3
                response['msg'] = '密码错误'
            else:
                cookie['session'] = rows[0]['SessionId']
                cookie['session']['expires'] = 30 * 60
                cookie['user_name'] = username
                cookie['user_id'] = rows[0]['id']
    finally:
        db.close()

viewer.set_cookie(cookie)
response['code'] = res
if res == 1:
    viewer.add_view('header', params)
    viewer.add_view('login', params)
    viewer.output()
else:
    viewer.output(response)
