#!C:\Program Files\Python27\python.exe
# coding=utf-8

import cgi
import os
import Cookie
import hashlib

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
    passwd = form.getfirst('password')
    
    db = dbconnector.DbConnector()
    try:
        rows = db.query("select * from users where UserName=%s", [username])
        if len(rows) == 0 or len(rows) > 1:
            res = -2
            params['login_msg'] = '该用户不存在'
        else:    
            md5 = hashlib.md5()
            md5.update(passwd)
            md5.update(rows[0]['Salt'])
            hash_passwd = md5.hexdigest()
            if hash_passwd != rows[0]['Password']:
                res = -3
                params['login_msg'] = '密码错误'
            else:
                cookie['session'] = rows[0]['SessionId']  
                cookie['session']['expires'] = 30 * 60
                cookie['user_name'] = username
                cookie['user_id'] = rows[0]['id']           
                params['welcome'] = '登录成功，你好 '+username
                params['reg'] = username
                params['reg_url'] = 'index.py'
                params['login'] = '注销'
                params['login_url'] = 'logout.py'
                params['upload_btn'] = '''<a href="%s/src/upload.py" class="btn btn-info">上传头像</a>'''%DOCUMENT_ROOT
                params['token_str'] = '您的api token为%s<br>访问url：yagra/src/api.py?token=%s即可使用' % (rows[0]['Token'], rows[0]['Token'] )
                params['img_path'] = db.query('''select FileName from users join avatars 
                    on AvatarId = avatars.id where users.id = %s''', [rows[0]['id']])[0]['FileName']
    except Exception, e:
        os.stderr.write("database error", e)
    finally:
        db.close()
    

print cookie
print '\n'
viewer.load('header', params)
if res != 0:
    viewer.load('login', params)
else:
    print '<meta http-equiv="refresh" content="0;url=http://localhost/cgi-bin/yagra/src/index.py">'
    viewer.load('index', params) 