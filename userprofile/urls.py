# /userprofile/urls.py

from django.urls import path

import userprofile
from . import views

app_name = 'userprofile'

urlpatterns = [

path('login/', views.user_login, name='login'),
path('logout/', views.user_logout, name='logout'),
path('register',views.user_register,name='register'),
path('user-delete/<int:id>',views.user_delete,name='delete')

# path('index/',index),

]