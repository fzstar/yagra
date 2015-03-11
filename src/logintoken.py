#!/usr/bin/python
# coding=utf-8

import cgi
import json

import dbconnector
from hashutil import HashUtil

form = cgi.FieldStorage()
username = form.getfirst('user_name')

db = dbconnector.DbConnector()
response = {'code' : 0, 'token' : ''}
try:
    token = HashUtil.get_random_token()
    sql = 'update users set LoginToken = %s where UserName = %s';
    sql_params = [token, username]
    db.execute(sql, sql_params)
    response['token'] = token
except Exception, e:
    raise e
    resonse['code'] = -1
finally:
    db.close()

header = 'Content-Type: text/html; charset=utf-8'    
print(header)
print '\n'
print json.dumps(response)