#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/18 10:15
# @Author  : Ryu
# @Site    : 
# @File    : urls.py
# @Software: PyCharm


from django.urls import path, include

from . import views

urlpatterns = [
    path('display/',views.display,name='display'),
    path('intro/',views.intro,name='intro'),
    path('ms/',views.ms,name='ms'),
    path('captcha/',views.get_captcha,name='captcha'),
    path('trance/',views.trance_captcha,name='trance'),
    path('check/',views.check_capt,name='check'),
    path('key_up/',views.key_up,name='key_up')

]