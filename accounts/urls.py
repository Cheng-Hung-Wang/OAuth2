#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from django.conf.urls import url
from django.conf import settings
from .views import login
from .views import callback

urlpatterns = [
  url(r'^login', login),
  url(r'^%s'%settings.CALLBACK_PATH.split('/')[-1], callback),
]

