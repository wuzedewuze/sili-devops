#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/7/20 13:50
# @Author : "wuyang"
# @Email : wuyang_229@126.com
# @File : test.py
# @Software: PyCharm

import os, django
from django.contrib.auth import get_user_model
os.environ['DJANGO_SETTINGS_MODULE'] = 'sili_devops.settings'
django.setup()


def get_users(base_name, user_number):
    users = []
    for i in range(user_number):
        username = '{}-{}'.format(base_name, i)
        email = '{}@xiniaoyun.com'.format(username)
        user = {'username': username, 'email':email}
        users.append(user)
    return users


if __name__ == '__main__':
    User = get_user_model()
    base_name = 'wuyang'
    user_number = 50
    users = get_users(base_name, user_number)
    for user in users:
        user_obj = User(**user)
        user_obj.save()

