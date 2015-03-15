#!/usr/bin/python
# coding=utf-8

import cgi
import os
import sys
import viewer
import Cookie
import dbconnector
import config
import session
import cgitb
cgitb.enable()

DOCUMENT_ROOT = config.DOCUMENT_ROOT
viewer = viewer.Viewer()
    
if ('REQUEST_METHOD' in os.environ and os.environ['REQUEST_METHOD'] == 'GET'):
    params = {'site_url' : DOCUMENT_ROOT, 'reg' : '注册', 'reg_url' : 'reg', \
              'login' : '登录', 'login_url' : 'login', 'welcome' : '你好',\
              'img_path' : 'default.jpg'}
    db = dbconnector.DbConnector()
    try:
        session = session.get_session(db)
        if session != None:
            params['welcome'] = '你好 '+session['user_name'].value
            params['reg'] = session['user_name'].value
            params['reg_url'] = 'index'
            params['login'] = '注销'
            params['login_url'] = 'logout'
            params['upload_btn'] = '''<a href="%s/upload" class="btn btn-info">头像设置</a>'''%DOCUMENT_ROOT
            rows = db.query('''select FileName,Token from users join avatars 
                on AvatarId = avatars.id where users.id = %s''', [session['user_id'].value])
            params['img_path'] = rows[0]['FileName']
            params['token_str'] = '您的api token为%s<br>访问url：{主机名}/api?token=%s即可使用' % (rows[0]['Token'], rows[0]['Token'] )
    finally:
        db.close()
    
    viewer.add_view('header', params)
    viewer.add_view('index', params)
    viewer.output()
