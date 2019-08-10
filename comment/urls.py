# /comment/urls.py

from django.urls import path

import userprofile
from . import views

app_name = 'userprofile'

urlpatterns = [

    path('post-comment/<int:article_id>/', views.post_comment, name='post_comment'),
]