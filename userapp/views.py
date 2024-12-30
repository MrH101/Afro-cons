from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

class LoginView(View):
    def get(self, request):
        return render(request, 'page-user-login.html')

    def post(self, request):
        user=authenticate(username=request.POST.get('username'),
                          password=request.POST.get('password'))

        if user is None:
            return redirect('/user/login/')
        login(request, user)
        return redirect('/asosiy/')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/user/login/')

class RegisterView(View):
    def get(self, request):
        return render(request, 'page-user-register.html')


