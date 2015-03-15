#!/usr/bin/python
# coding=utf-8

import cgi

import dbconnector
import session
import viewer

viewer = viewer.Viewer()
form = cgi.FieldStorage()
img_id = form.getfirst('img_id')
response = {'code' : -1, 'msg' : '修改失败，请重试'}
try:
    db = dbconnector.DbConnector()
    session = session.get_session(db)
    if session == None:
        response['code'] = 1
        response['msg'] = '请先登录'
    else:
        db.execute('update users set AvatarId = %s where id = %s', [img_id, session['user_id'].value])
        response['code'] = 0
        response['msg'] = '修改成功'
finally:
    db.close()

viewer.output(response)