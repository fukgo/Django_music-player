from django.contrib.auth import logout
from django.contrib import messages

from io import BytesIO
from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm, ProfileForm
from utils import generate_code
from .models import CustomUser, Profile
def auth_code(request):
    img, code_string = generate_code.check_code()
    # print(code_string)
    stream = BytesIO()
    request.session['code'] = code_string
    img.save(stream, 'png')
    print(img, code_string)
    stream.getvalue()
    return HttpResponse(stream.getvalue())

from django.http import JsonResponse

def login_out(request):
    messages.info(request, '您已退出登录')
    logout(request)
    return JsonResponse({'success': True})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            code = form.cleaned_data.get('code')
            if request.session.get('code') != code:
                form.add_error('code', '验证码输入错误')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('song:home')
            else:
                form.add_error('username', '账号或密码输入错误')
        else:
            print(form.errors)
            print(form.cleaned_data)
            form.add_error('username', '账号或密码输入错误')
    else:
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form,'error': form.errors})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if CustomUser.objects.filter(username=username).exists():
                form.add_error('username', '用户名已存在')
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            messages.info(request, '成功登录。')
            login(request, new_user)
            return redirect('song:home')
        else:
            print(form)
            form.add_error('', '输入表单有误')
    form = RegisterForm()
    return render(request, 'User/register.html', {'form': form,'error':form.errors})

class UserProfile(View):
    def get(self, request, id):
        user = CustomUser.objects.get(id=id)
        profile = user.profile
        return render(request, 'Profile/user_prifile.html', {'profile': profile, 'user': user})

    def post(self, request,profile_id):
        profile = Profile.objects.get(id=profile_id)
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user:profile', profile_id)
        return render(request, 'Profile/user_prifile.html', {'form': form,'error':form.errors})

