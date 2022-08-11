from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.models import User

#로그인 함수
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'bad_login.html')
    else:
        return render(request, 'login.html')

#로그아웃
def logout(request):
    auth.logout(request)
    return redirect('home')

#회원가입
def signup(request):
    if request.method == "POST":
        if request.POST['password'] == request.POST['repeat']:
            new_user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            auth.login(request, new_user)
            return redirect('home')
    return render(request, 'signup.html')
