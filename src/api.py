#!C:\Program Files\Python27\python.exe
# coding=utf-8

import cgi
import os

import dbconnector
import config
import cgitb
cgitb.enable()

DOCUMENT_ROOT = config.DOCUMENT_ROOT
UPLOAD_FILE_PATH = config.UPLOAD_FILE_PATH

try: # Windows needs stdio set for binary mode.  
    import msvcrt  
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0  
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1  
except ImportError:  
    pass  

form = cgi.FieldStorage()
token = form.getfirst('token')

if token != None:
    db = dbconnector.DbConnector()
    rows = db.query('''select FileName from users join avatars on users.AvatarId = avatars.id
                       where Token = %s''', [token])
    if len(rows) == 1:
        file_name = rows[0]['FileName']
        file_type = file_name.split('.')[-1]
        header = 'Content-Type: image/%s;\n' % file_type
        file = open(UPLOAD_FILE_PATH+'/'+file_name, 'rb')
        file_data = file.read()
        file.close()
        print header
        print file_data
        exit(0)

header = 'Content-Type: text/html; charset=utf-8\n\n'
print header
print 'token无效'
        