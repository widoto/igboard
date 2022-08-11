import imp
from django.contrib import auth
from django.contrib.auth import authenticate
#from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import User
# Create your views here.
# 회원가입
def signup(request):
    if request.method == 'POST':
        #if request.POST['password1'] == request.POST['password2']:
            user_id = request.POST.get('id','')
            user_pw = request.POST.get('pw','')
            user = User(
                user_id=user_id,
                user_pw=user_pw,
            )
            user.save()
        #return render(request, 'signup.html')
    return render(request, 'signup.html')

# 로그인
def login(request):
    if request.method == 'POST':
        userid = request.POST.get('id')
        password = request.POST.get('pw')
        user = authenticate(request, user_id=userid, user_pw=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'login.html')


# 로그아웃
def logout(request):
    auth.logout(request)
    return redirect('home')

# home
def home(request):
    return render(request, 'home.html')