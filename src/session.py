#!/usr/bin/python
# coding=utf-8

import os
import Cookie


def get_session(db):
    if 'HTTP_COOKIE' in os.environ:
        cookie = Cookie.SimpleCookie(os.environ['HTTP_COOKIE'])
        if 'session' not in cookie.keys():
            return None
        session = cookie['session'].value
        sql = 'select * from users where UserName = %s AND SessionId = %s'
        param = [cookie['user_name'].value, session]
        rows = db.query(sql, param)
        if len(rows) == 1:
            return cookie
    return None
