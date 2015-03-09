#!/usr/bin/python
#!/usr/bin/python

import cgi
import os
import sys
import hashlib
import time

import viewer
import dbconnector
import config
import session
import cgitb
cgitb.enable()

SESSION_KEY = config.SESSION_KEY
DOCUMENT_ROOT = config.DOCUMENT_ROOT
MAXBYTES = config.MAX_IMAGE_SIZE
UPLOAD_FILE_PATH = config.UPLOAD_FILE_PATH
header = 'Content-Type: text/html; charset=utf-8'
viewer = viewer.Viewer()
    
try: # Windows needs stdio set for binary mode.  
    import msvcrt  
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0  
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1  
except ImportError:  
    pass  
    
res_msg = {-1 : '文件类型不正确', -2 : '文件大小超过上限', -3 : '上传失败'}
    
def save_file(image, username):
    if not (image.filename and image.file):
        return -3
    filename = str(int(time.time()*1000))   #字符串形式的当前时间戳
    upfile = image.file
    extension = image.filename.split(".")[-1]
    if extension not in ['jpg', 'png']:
        return -1
    filename = username + "_" + filename + "." + extension    #文件名为 用户名_时间戳.扩展名
    file_data = upfile.read(MAXBYTES+10)
    if len(file_data) > MAXBYTES:
        return -2
    save_file = open(UPLOAD_FILE_PATH+"/"+filename,'w+b')
    save_file.write(file_data)
    save_file.close()
    return filename

print(header)
res = -1; 
params = {'site_url' : DOCUMENT_ROOT, 'reg' : '注册', 'reg_url' : 'reg.py', \
          'login' : '登录', 'login_url' : 'login.py', 'welcome' : '你好',\
          'img_path' : 'default.jpg'}
db = dbconnector.DbConnector()
try:
    session = session.get_session(db)
    if session == None:
        res = 1
        params['welcome'] = '请先登录'
    else:
        params['reg'] = session['user_name'].value
        params['reg_url'] = 'index.py'
        params['login'] = '注销'
        params['login_url'] = 'logout.py'
        params['img_path'] = db.query('''select FileName from users join avatars 
              on AvatarId = avatars.id where users.id = %s''', [session['user_id'].value])[0]['FileName']
        if ('REQUEST_METHOD' in os.environ and os.environ['REQUEST_METHOD'] == 'POST'):
            form = cgi.FieldStorage()
            image = form['image']
            filename = save_file(image, session['user_name'].value)
            if type(filename) != int:  
                res = 0
                params['upload_msg'] = '上传成功'
                sql = 'insert into avatars(UserId, FileName) values (%s,%s)'
                sql_params = [session['user_id'].value, filename]
                avatar_id = db.execute(sql, sql_params)
                sql = 'update users set AvatarId = %s where id = %s'
                sql_params = [avatar_id, session['user_id'].value]
                db.execute(sql, sql_params)
                params['img_path'] = filename
            else:         
                params['upload_msg'] = res_msg[filename]
except Exception, e:
    print("error", e)
finally:
    db.close()
    

print '\n'
viewer.load('header', params)
if res == 0:
    print '<meta http-equiv="refresh" content="0;url=http://localhost/cgi-bin/yagra/src/upload.py">'
    viewer.load('upload', params)
elif res == 1:
    viewer.load('index', params)
else:
    viewer.load('upload', params)