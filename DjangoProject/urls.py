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

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import blog
import userprofile
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
    path('article/',blog.views.home,name='home'),
    path('article/articleList/',blog.views.articleList,name='articleList'),
    path('article/article-detail/<int:id>/',blog.views.article_detail,name='article_detail'),

    path('article-create/',blog.views.article_create,name='article_create'),
    path('article/article-delete/<int:id>/',blog.views.article_delete,name='article_delete'),
    path('article/article-update/<int:id>/',blog.views.article_update,name='article_update'),
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
    path('password-reset/', include('password_reset.urls')),

    # path('login/',userprofile.views.user_login,name='userLogin'),



]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
