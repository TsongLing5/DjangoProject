"""DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.conf.urls import url
from django.contrib import admin
from django.urls import path

import blog
from DjangoProject.settings import BASE_DIR
from blog.views import index, main,test

# from blog.views import main

urlpatterns = [

    path('admin/', admin.site.urls),
    path('index/',index),
    path('main/',main),
    url(r'^$', blog.views.home, name='home'),
    path('test/<str:a>/',blog.views.test,name='test'),
    path('test/<int:a>/',blog.views.test,name='test'),
    path('haha/',blog.views.home,name='home'),
    path('article/articleList',blog.views.articleList,name='articleList'),
    path('article/article-detail/<int:id>/',blog.views.article_detail,name='article_detail')



]
