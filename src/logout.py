#!/usr/bin/python
# coding=utf-8

import cgi
import os
import Cookie
import hashlib

import viewer
import config
import cgitb
cgitb.enable()

SESSION_KEY = config.SESSION_KEY
DOCUMENT_ROOT = config.DOCUMENT_ROOT
viewer = viewer.Viewer()
cookie = Cookie.SimpleCookie()

params = {'site_url' : DOCUMENT_ROOT, 'reg' : '注册', 'reg_url' : 'reg', \
          'login' : '登录', 'login_url' : 'login', 'welcome' : '你好',\
          'img_path' : 'default.jpg'}

cookie['session'] = ''
cookie['user_name'] = ''
cookie['user_id'] = ''  

viewer.set_cookie(cookie)
viewer.add_view('header', params)
viewer.add_view('index', params)
viewer.output()
