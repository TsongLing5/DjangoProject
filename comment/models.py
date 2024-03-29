from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from blog.models import ArticlePost


class Comment(models.Model):
    article=models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    body=RichTextField()
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('created',)

    def __str__(self):
        return self.body[:20]
