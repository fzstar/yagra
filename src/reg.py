#!C:\Program Files\Python27\python.exe
# coding=utf-8

import cgi
import os
import sys
import hashlib
import hmac
import time
import Cookie

import viewer
import dbconnector
import config

SESSION_KEY = config.SESSION_KEY
DOCUMENT_ROOT = config.DOCUMENT_ROOT
header = 'Content-Type: text/html; charset=utf-8'
viewer = viewer.Viewer()
cookie = Cookie.SimpleCookie()

def get_salt(passwd):
    salt = hashlib.md5(str(time.time())).hexdigest()
    md5 = hashlib.md5()
    md5.update(passwd)
    md5.update(salt)
    hash_passwd = md5.hexdigest()
    return [hash_passwd, salt]
    
def get_session_id(username):
    return hmac.new(SESSION_KEY, username).hexdigest()

print(header)
res = 0;
params = {'site_url' : DOCUMENT_ROOT, 'reg' : '注册', 'reg_url' : 'reg.py', \
          'login' : '登录', 'login_url' : 'login.py', 'welcome' : '你好',\
          'img_path' : 'default.jpg'}

if ('REQUEST_METHOD' in os.environ and os.environ['REQUEST_METHOD'] == 'GET'):
    res = -1
else:
    form = cgi.FieldStorage()
    username = form.getfirst('user_name')
    passwd = form.getfirst('passwd')
    confirm_passwd = form.getfirst('confirm_passwd')
    if passwd != confirm_passwd:
        res = -2
        params['reg_msg'] = '两次输入的密码不一致'
    else:    
        db = dbconnector.DbConnector()
        try:
            if (db.count("select count(*) from users where UserName=%s", [username]) > 0):
                res = -3
                params['reg_msg'] = '用户名已存在'
            else:    
                sql = "insert into users(UserName,Password,Salt,SessionId) values (%s,%s,%s,%s)"
                salt_res = get_salt(passwd)
                sid = get_session_id(username)
                sql_params = [username, salt_res[0], salt_res[1], sid]
                user_id = db.execute(sql, sql_params)
                cookie['session'] = sid
                cookie['session']['expires'] = 30 * 60
                cookie['user_name'] = username
                cookie['user_id'] = user_id
                
                params['welcome'] = '注册成功，你好 '+username
                params['reg'] = username
                params['reg_url'] = 'index.py'
                params['login'] = '注销'
                params['login_url'] = 'logout.py'
                params['upload_btn'] = '''<a href="%s/src/upload.py" class="btn btn-info">上传头像</a>'''%DOCUMENT_ROOT
        except Exception, e:
            print '\n\n'
            print("database error", e)
        finally:
            db.close()

print cookie
print '\n'
viewer.load('header', params)
if res != 0:
    viewer.load('reg', params)
else:
    viewer.load('index', params)
