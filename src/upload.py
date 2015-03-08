#!C:\Program Files\Python27\python.exe
#!coding=utf-8

import cgi
import os
import hashlib

import viewer
import dbconnector
import config
import session

SESSION_KEY = config.SESSION_KEY
DOCUMENT_ROOT = config.DOCUMENT_ROOT
MAXBYTES = config.MAX_IMAGE_SIZE
UPLOAD_FILE_PATH = config.UPLOAD_FILE_PATH
header = 'Content-Type: text/html; charset=utf-8'
viewer = viewer.Viewer()
    
try: # Windows needs stdio set for binary mode.  
    import msvcrt  
    import uuid  
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0  
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1  
except ImportError:  
    pass  
    
def save_file(image, username):
    filename = image.filename
    upfile = image.file
    extension = filename.split(".")[-1]
    if extension not in ['jpg', 'png']:
        return -1
    filename = username+"_"+filename
    file_data = upfile.read()
    
    save_file = open(UPLOAD_FILE_PATH+"/"+filename,'w+b')
    save_file.write(file_data)
    save_file.close()
    return filename

print(header)
res = 0;
params = {'site_url' : DOCUMENT_ROOT, 'reg' : '注册', 'reg_url' : 'reg.py', \
          'login' : '登录', 'login_url' : 'login.py', 'welcome' : '你好',\
          'img_path' : 'default.jpg'}
db = dbconnector.DbConnector()
try:
    session = session.get_session(db)
    if ('REQUEST_METHOD' in os.environ and os.environ['REQUEST_METHOD'] == 'GET'):
        if session == None:
            res = 1
            params['welcome'] = '请先登录'
        else:
            res = -1
            params['reg'] = session['user_name'].value
            params['reg_url'] = 'index.py'
            params['login'] = '注销'
            params['login_url'] = 'logout.py'
    else:    
        form = cgi.FieldStorage()
        if session == None:
            res = 1
            params['welcome'] = '请先登录'
        else:
            image = form['image']
            if image.file:
                filename = save_file(image, session['user_name'].value)
                if filename == -1:
                    res = -1
                    params['upload_msg'] = '文件类型不正确'
                elif filename == -2:
                    res = -1
                    params['upload_msg'] = '文件大小超过上限'
                else:
                    res = -1
                    params['upload_msg'] = 'ok'
            else:
                res = -1
                params['upload_msg'] = '上传失败'
except Exception, e:
    print '\n\n'
    print("database error", e)
finally:
    db.close()
    

print '\n'
if 'debug' in params:
    print params['debug']
viewer.load('header', params)
if res != 1:
    viewer.load('upload', params)
else:
    viewer.load('index', params)