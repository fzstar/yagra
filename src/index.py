#!C:\Program Files\Python27\python.exe
# coding=utf-8

import cgi
import os
import viewer
import Cookie
import dbconnector
import config
import session

DOCUMENT_ROOT = config.DOCUMENT_ROOT
header = 'Content-Type: text/html; charset=utf-8\n\n'
viewer = viewer.Viewer()
    
if ('REQUEST_METHOD' in os.environ and os.environ['REQUEST_METHOD'] == 'GET'):
    print(header)
    params = {'site_url' : DOCUMENT_ROOT, 'reg' : '注册', 'reg_url' : 'reg.py', \
              'login' : '登录', 'login_url' : 'login.py', 'welcome' : '你好',\
              'img_path' : 'default.jpg'}
    db = dbconnector.DbConnector()
    try:
        session = session.get_session(db)
        if session != None:
            params['welcome'] = '你好 '+session['user_name'].value
            params['reg'] = session['user_name'].value
            params['reg_url'] = 'index.py'
            params['login'] = '注销'
            params['login_url'] = 'logout.py'
            params['upload_btn'] = '''<a href="%s/src/upload.py" class="btn btn-info">上传头像</a>'''%DOCUMENT_ROOT
            params['img_path'] = db.query('''select Path from users join avatars 
                on AvatarId = avatars.id where users.id = %s''', [session['user_id'].value])[0]['Path']
    except Exception, e:
        print ("Error", e)
    finally:
        db.close()
    
    viewer.load('header', params)
    viewer.load('index', params)

