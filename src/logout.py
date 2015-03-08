#!C:\Program Files\Python27\python.exe
# coding=utf-8

import cgi
import os
import Cookie
import hashlib

import viewer
import config

SESSION_KEY = config.SESSION_KEY
DOCUMENT_ROOT = config.DOCUMENT_ROOT
header = 'Content-Type: text/html; charset=utf-8'
viewer = viewer.Viewer()
cookie = Cookie.SimpleCookie()
    
print(header)
params = {'site_url' : DOCUMENT_ROOT, 'reg' : '注册', 'reg_url' : 'reg.py', \
          'login' : '登录', 'login_url' : 'login.py', 'welcome' : '你好',\
          'img_path' : 'default.jpg'}

cookie['session'] = ''
cookie['user_name'] = ''
cookie['user_id'] = ''  

print cookie
print '\n'
viewer.load('header', params)
viewer.load('index', params)