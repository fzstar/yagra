#!/usr/bin/python
# coding=utf-8

import cgi
import os

import viewer
import dbconnector
import config
import cgitb
cgitb.enable()

DOCUMENT_ROOT = config.DOCUMENT_ROOT
UPLOAD_FILE_PATH = config.APP_ROOT + '/img/'

try:    # Windows needs stdio set for binary mode.
    import msvcrt
    msvcrt.setmode(0, os.O_BINARY)     # stdin  = 0
    msvcrt.setmode(1, os.O_BINARY)     # stdout = 1
except ImportError:
    pass

viewer = viewer.Viewer()
form = cgi.FieldStorage()
token = form.getfirst('token')

if token is not None:
    db = dbconnector.DbConnector()
    rows = db.query('''select FileName from users join avatars on users.AvatarId = 
                       avatars.id where Token = %s''', [token])
    if len(rows) == 1:
        file_name = rows[0]['FileName']
        file_type = file_name.split('.')[-1]

        file = open(UPLOAD_FILE_PATH + file_name, 'rb')
        file_data = file.read()
        file.close()

        header = 'Content-Type: image/%s;\nCache-Control: max-age=300\n' 
                  % file_type
        print header
        print file_data
        db.close()
        exit(0)

viewer.output()
print 'invalid token'
