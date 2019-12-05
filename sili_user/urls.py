#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/19 15:23
# @Author : "wuyang"
# @Email : wuyang_229@126.com
# @File : urls.py
# @Software: PyCharm
# from . views import UserInfoViewSet
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter,SimpleRouter
from .views import  UserViewSet, UserInfoViewSet
users_router = DefaultRouter() #trailing_slash=False 去掉末尾的斜杠
users_router.register(r'user', UserViewSet, base_name="user")               # 超级管理员 管理用户信息
users_router.register(r'userinfo', UserInfoViewSet, base_name="userinfo")   # 普通用户查看和管理自己信息

# 定义app_name 外部url指定app
app_name = 'user_api'
urlpatterns = [
    # path('userinfo/<int:pk>/', UserInfoViewSet.as_view(),name='user-info'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
#  添加注册的路由
urlpatterns += users_router.urls
