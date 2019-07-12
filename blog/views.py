from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

from blog.models import ArticlePost

userlist=[]
def index(request):
    # return HttpResponse('MineMine博客首页')
    if request.method == 'POST':
        password = request.POST.get('password')
        username= request.POST.get('username')
        temp={'user':username,'pwd':password}
        userlist.append(temp)
        print(username,password)
    return render(request,'index.html',{'data':userlist})

def main(request):
    return  HttpResponse("ようこそ！")

def test(request,a):
    return HttpResponse("AHAHA"+str(a))

def home(request):
    articles = ArticlePost.objects.all()
    context = {'articles': articles}
    return render(request, 'article/articleList.html', context)

def articleList(request):
    articles=ArticlePost.objects.all()
    context = {'articles': articles}
    return  render(request,'article/articleList.html',context)

def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    context = {'article':article}

    # article = ArticlePost.objects.get(id=id)
    # # 需要传递给模板的对象
    # context = {'article': article}
    return render(request, 'article/detail.html', context)
