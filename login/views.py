from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from .models import User

# Create your views here.


def homeview(request, *args, **kwargs):
    return render(request, 'login-register.html')


def forgetview(request, *args, **kwargs):
    return render(request, 'forgot-password.html')


def openview(request, *args, **kwargs):
    return render(request, 'index.html')


def ticket(request, *args, **kwargs):
    if request.method == 'POST':
        send_mail('Retailer Request', 'LET ME INNNNNNNNNNNNNN',
                  'retailiiti@gmail.com', ['retailiiti@gmail.com'], fail_silently=False)
        return HttpResponse('Your request is sent to the admins.')
    else:
        return render(request, 'ticket.html')


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
        messages.info(request, 'Wrong password')
        return redirect('../')


def welcome(request, *args, **kwargs):
    return render(request, 'Welcome.html')
