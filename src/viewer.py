#!/usr/bin/python
# coding=utf-8

import re
import config

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Viewer(object):
    HTML_ROOT = config.HTML_ROOT
    def load(self, view_name, params):
        def re_sub(m):
            if m.group(1) in params.keys():
                return params[m.group(1)]
            else:
                return ''
        html_str = self.__load_file(view_name)
        #for key in params.keys():
        #    html_str = html_str.replace('%' + key + '%', params[key])
        p = re.compile(r'%([\d\w_]+)%+')
        html_str = p.sub(re_sub, html_str)
        print html_str
    
    def __load_file(self, file_name):
        try:
            html = open(self.HTML_ROOT + '/' + file_name+'.html')
            return html.read()
        except IOError, e:
            print('Read View File Error.', e)
            return ''
        
if __name__ == '__main__':
    params = {'site_url' : '/cgi-bin/yagra', 'reg' : '注册'}
    viewer = Viewer()
    viewer.load('header', params)
    
