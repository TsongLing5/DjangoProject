from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from userprofile.forms import UserLoginForm, UserRegisterForm, ProfileForm


# Create your views here.
from userprofile.models import Profile


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
                return redirect("articleList")
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

@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自动生成的字段
    profile = Profile.objects.get(user_id=id)




    if request.method == 'POST':
        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")

        # profile_form = ProfileForm(data=request.POST,request.FILES)
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            # 取得清洗后的合法数据
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']

            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]
                print(request.FILES)

            profile.save()

            # 带参数的 redirect()
            return redirect("userprofile:edit", id=id)
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")

    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = { 'profile_form': profile_form, 'profile': profile, 'user': user }
        return render(request, 'edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")