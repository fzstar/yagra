#!/usr/bin/python
# coding=utf-8

import hashlib
import hmac
import time
import random

import config


class HashUtil(object):
    SESSION_KEY = config.SESSION_KEY

    @classmethod
    def get_salt_passwd(cls, passwd, salt):
        return HashUtil.get_md5(passwd, salt)

    @classmethod
    def gen_salt(cls):
        return HashUtil.get_md5(str(time.time()))

    @classmethod
    def get_session_id(cls, username):
        return hmac.new(HashUtil.SESSION_KEY, username).hexdigest()

    @classmethod
    def get_random_token(cls):
        ran = random.random()
        return HashUtil.get_md5(str(ran))

    @classmethod
    def get_md5(cls, *str):
        md5 = hashlib.md5()
        for item in str:
            md5.update(item)
        return md5.hexdigest()

if __name__ == '__main__':
    print HashUtil.get_md5('123', 'abc')
    print HashUtil.get_md5('123' + 'abc')
