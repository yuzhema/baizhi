#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/18 10:15
# @Author  : Ryu
# @Site    : 
# @File    : urls.py
# @Software: PyCharm




from django.contrib import admin
from django.urls import path, include

from user_app import views

urlpatterns = [
    path('login/',include(([path('page/',views.login_page,name='page'),
                            path('logic/',views.login_logic,name='logic')],'login'))),
    path('register/',include(([path('page/',views.register_page,name='page'),
                               path('logic/',views.register_logic,name='logic'),
                               path("ajax_reg/", views.ajax_test1, name="ajaxreg"),
                               path("show/", views.get_captcha, name="show"),
                               path('confirm/',views.user_confirm,name="confirm"),
                               path("checkcode/", views.checkcode, name="checkcode"),],'register'))),
]