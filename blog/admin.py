

from django.contrib import admin
from . import models
from .models import ArticlePost
from comment.models import Comment

# Register your models here.
admin.site.register(ArticlePost)
admin.site.register(Comment)