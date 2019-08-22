from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

from DjangoProject import settings
from blog.models import ArticlePost
from blog.forms import ArticlePostForm
from blog.models import ArticleColumn
import markdown

from comment.models import Comment
from userprofile.models import Profile
import configparser

# cfg_path = settings.CONF_DIR
# cf = configparser.ConfigParser()
# cf.read(cfg_path)
#
# settings.EMAIL_HOST_USER = cf.get("email_cfg", "email_host_user")  # 读取配置文件
# settings.DEFAULT_FROM_EMAIL=cf.get("email_cfg", "default_from_mail")
# settings.EMAIL_HOST_PASSWORD=cf.get("email_cfg", "email_password")
# print(settings.EMAIL_HOST_USER)
# print(settings.EMAIL_HOST_PASSWORD)
# print(settings.DEFAULT_FROM_EMAIL)
# print(mail_host)

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
    return redirect("articleList") #将网页重新指向articleList 这个页面，跳转
    # articles = ArticlePost.objects.all()
    # context = {'articles': articles}
    # return render(request, 'article/articleList.html', context)

def articleList(request):
    search=request.GET.get('search')
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    if search:
        if request.GET.get('order') == 'total_views':
            articleList = ArticlePost.objects.filter(Q(title__icontains=search) | Q(body__icontains=search)).order_by('-total_views')
            order='total_views'
        else:
            articleList=ArticlePost.objects.filter(Q(title__icontains=search)|Q(body__icontains=search))
            order='normal'
    else:
        # search=''
        if request.GET.get('order') == 'total_views':
            articleList = ArticlePost.objects.all().order_by('-total_views')
            order='total_views'
        else:
            articleList=ArticlePost.objects.all()
            order='normal'

    pagionator=Paginator(articleList,6)
    page=request.GET.get('page')
    articles=pagionator.get_page(page)
    if request.user.is_authenticated:
        context = {'articles': articles,'order':order,'search':search,'profile':profile}
    else:
        context = {'articles': articles, 'order': order, 'search': search}
    return  render(request,'article/articleList.html',context)

def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    comments=Comment.objects.filter(article=id)

    # comments = Comment.objects.filter(article=id)

    profile = Profile.objects.get(user=request.user)
    # print(profile.avatar.url)
    # print(request.user)

    article.total_views +=1
    article.save(update_fields=['total_views'])

    md = markdown.Markdown(
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        ]
    )
    # article.body = markdown.markdown(article.body,
    #                                  extensions=[
    #                                      # 包含 缩写、表格等常用扩展
    #                                      'markdown.extensions.extra',
    #                                      # 语法高亮扩展
    #                                      'markdown.extensions.codehilite',
    #                                      'markdown.extensions.TOC',
    #                                  ])
    article.body = md.convert(article.body)

    context = {'article':article,'toc': md.toc,'comments':comments,'profile':profile}

    # article = ArticlePost.objects.get(id=id)
    # # 需要传递给模板的对象
    # context = {'article': article}
    return render(request, 'article/detail.html', context)

def article_create(request):
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)
            # 将新文章保存到数据库中
            if request.POST['column'] != None:
                new_article.column=ArticleColumn.objects.get(id=request.POST['column'])

            else:
                new_article.column=None

            new_article.save()
            article_post_form.save_m2m()

            return redirect('/') #重新定向回主页
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")#此处建议用错误弹窗提高体验也使得表单数据不易丢失
    else:
        article_post_form=ArticlePostForm()
        columns=ArticleColumn.objects.all()
        context={'article_post_form': article_post_form,'columns':columns}
        return render(request,'article/createpage.html',context)

def article_delete(request,id):
    article=ArticlePost.objects.get(id=id)
    if request.user == article.author:
        article.delete()
        return redirect('/')  #delete 完成 return home
    else:
        return HttpResponse('错误，无权修改')

def article_update(request,id):
    article=ArticlePost.objects.get(id=id)
    if request.user == article.author:
        if request.method == "POST":
            article_post_form = ArticlePostForm(data=request.POST)
            if article_post_form.is_valid():
                article.title=request.POST['title']
                article.body = request.POST['body']
                tags=request.POST['tags']
                if(tags):
                    print(tags)
                    print(article.tags.all)
                    article.tags.clear()
                    for tag in tags.split(","):
                        article.tags.add(tag)
                        print(tag)

                # article.tags.set(request.POST['tags'],clear=True)
                # print(request.POST['title'])
                # print(article.body)
                if(request.POST['column'] != 'none'):
                    article.column=ArticleColumn.objects.get(id=request.POST['column'])
                else:
                    article.column=None
                article.save()

                return redirect("/article/article-detail/"+str(id))
            else:
                return HttpResponse("表???")
        else:  #metho GET
            article_get_form = ArticlePostForm()
            columns = ArticleColumn.objects.all()

            article_get_form.body=article.body
            context = {'article':article,'article_get_form': article_get_form,'columns':columns}
            return render(request, 'article/createpage.html', context)
    else:
        return HttpResponse("无权修改")



def userLogin(request):
    return render(request, 'article/login.html')