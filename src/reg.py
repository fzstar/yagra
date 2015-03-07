#!C:\Program Files\Python27\python.exe
# coding=utf-8

import cgi
import os
import viewer

DOCUMENT_ROOT = '/cgi-bin/yagra'
header = 'Content-Type: text/html; charset=utf-8\n\n'
viewer = viewer.Viewer()

if ('REQUEST_METHOD' in os.environ and os.environ['REQUEST_METHOD'] == 'GET'):
    print(header)
    head_params = {'site_url' : DOCUMENT_ROOT, 'reg' : '注册'}
    viewer.load('header', head_params)
    params = {'site_url' : DOCUMENT_ROOT}
    viewer.load('reg', params)

