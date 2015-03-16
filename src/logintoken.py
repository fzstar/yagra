#!/usr/bin/python
# coding=utf-8

import cgi

import viewer
import dbconnector
from hashutil import HashUtil

viewer = viewer.Viewer()
form = cgi.FieldStorage()
username = form.getfirst('user_name')

db = dbconnector.DbConnector()
response = {'code': 0, 'token': ''}
try:
    token = HashUtil.get_random_token()
    sql = 'update users set LoginToken = %s where UserName = %s'
    sql_params = [token, username]
    db.execute(sql, sql_params)
    response['token'] = token
except Exception, e:
    resonse['code'] = -1
    raise e
finally:
    db.close()

viewer.output(response)
