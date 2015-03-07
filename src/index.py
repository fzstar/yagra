#!C:\Program Files\Python27\python.exe

import sys
import cgi
import os
import datetime
import json

HTML_PATH = 'D:/Tools/xampp/cgi-bin/src/static'
header = 'Content-Type: text/html\n\n'

if ('REQUEST_METHOD' in os.environ and os.environ['REQUEST_METHOD'] == 'GET'):
    try:
        with open(HTML_PATH + '/index.html') as html:
            print(header)     # HTML is following
            print(html.read())
    except IOError, e:
        print('Error')

