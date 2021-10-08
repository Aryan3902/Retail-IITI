from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.auth.hashers import make_password, check_password
from .models import User

# Create your views here.


def homeview(request, *args, **kwargs):
    return render(request, 'login-register.html')


def forgetview(request, *args, **kwargs):
    return render(request, 'forgot-password.html')


def openview(request, *args, **kwargs):
    return render(request, 'index.html')


def signupauth(request, *args, **kwargs):
    Name = request.POST.get('Name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    password1 = request.POST.get('password1')

    userlist = User.objects.filter(email=email).values()
    if (len(userlist) == 0):
        if password != password1:
            messages.info(request, "Password does not match")
            return redirect('../')
        else:
            P = make_password(password)
            a = User()
            a.name = Name
            a.email = email
            a.password = P
            a.save()
            messages.info(request, "You are now signed up Try to login")
            return redirect('../')
    else:
        messages.info(request, "User already registered")
        return redirect('../')


def login(request, *args, **kwargs):
    email = request.POST.get('email')
    password = request.POST.get('password')
    username = request.POST.get('Name')
    userlist = User.objects.filter(email=email).values()
    userA = userlist[0]
    if check_password(password, userA['password']):
        print(userA['name'])
        return render(request, 'index.html', {'userMain': userA['name']})
        # return redirect('../home/', {'userMain': userA['name']})

    else:
        messages.info(request, 'Worng password')
        return redirect('../')
