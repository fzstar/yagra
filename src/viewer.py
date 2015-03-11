#!/usr/bin/python
# coding=utf-8

import re
import config

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Viewer(object):
    DOCUMENT_ROOT = config.DOCUMENT_ROOT
    HTML_ROOT = config.HTML_ROOT
    HOST_NAME = config.HOST_NAME
    def load(self, view_name, params):
        def re_sub(m):
            if m.group(1) in params.keys():
                return params[m.group(1)]
            else:
                return ''
        html_str = self.__load_file(view_name)
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
        
    def __load_file(self, file_name):
        try:
            html = open(self.HTML_ROOT + '/' + file_name+'.html')
            return html.read()
        except IOError, e:
            print('Read View File Error.', e)
            return ''
            
    def load_save_imgs(self, save_imgs):
        ret = ''
        for img in save_imgs:
            ret += '''<a href="#"><img class="img-thumbnail save-img" img-id="%s" src="%s/img/%s"></a>''' % (img['id'], self.DOCUMENT_ROOT, img['FileName'])
        return ret
        
    def set_redirect(self, url, time=0):
        print '<meta http-equiv="refresh" content="%d;url=http://%s/yagra/src/%s">' % (time, self.HOST_NAME, url)

if __name__ == '__main__':
    params = {'site_url' : '/cgi-bin/yagra', 'reg' : '注册'}
    viewer = Viewer()
    viewer.load('header', params)
    
