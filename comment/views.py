from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from blog.models import ArticlePost
from comment.forms import CommentForm



@login_required(login_url='/userprofile/login/')
def post_comment(request,article_id):
    article = get_object_or_404(ArticlePost, id=article_id)

    if request.method=='POST':
        comment=CommentForm(request.POST)
        if comment.is_valid():
            newComment=comment.save(commit=False)
            newComment.article=article
            newComment.user=request.user
            newComment.save()
            return redirect(article)
        else:
            HttpResponse('表格有误，请重写')
    else:
        HttpResponse("发布评论仅接受POST")

