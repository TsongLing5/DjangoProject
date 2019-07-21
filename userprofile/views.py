from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from userprofile.forms import UserLoginForm, UserRegisterForm


# Create your views here.


def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect("/")
            else:
                return HttpResponse("账号或密码输入有误。请重新输入~")
        else:
            return HttpResponse("账号或密码输入不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = { 'form': user_login_form }
        return render(request, 'login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

def user_logout(request):
    logout(request)
    return redirect('/')

def user_register(request):
    if request.method == "POST":
        userRegisterForm=UserRegisterForm(data=request.POST)
        if request.POST.get('password') == request.POST.get('password2'):
            pass
        else:
            return HttpResponse("密码不一致，请重新输入密码")
        if userRegisterForm.is_valid():
            newUser=userRegisterForm.save(commit=False)
            newUser.set_password(userRegisterForm.cleaned_data['password'])
            newUser.save()
            login(request,newUser)
            return redirect('/')
        else:
            # userRegisterForm.cleaned_data['password']
            return HttpResponse("输入的数据无效！请重新输入!")
    elif request.method == "GET":  #Get
        form=UserLoginForm()
        context={"form":form}
        return render(request, 'register.html',context)

@login_required(login_url='/userprofile/login')
def user_delete(request,id):
    user=User.objects.get(id=id)
    if(user== request.user):
        logout(request)
        user.delete()
        return redirect('/')
    else:
        return HttpResponse("Auth deny!")