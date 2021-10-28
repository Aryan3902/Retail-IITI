from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from .models import User
import random
import requests

# Create your views here.


def homeview(request, *args, **kwargs):
    return render(request, 'login-register.html')


def forgetview(request, *args, **kwargs):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')

        userlist = User.objects.filter(name=name, email=email).values()

        if len(userlist) > 0:
            users = User.objects.get(email=email)

            password = ""
            given = "QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuioplkjhgfdsazxcvbnm1234567890"
            for x in range(10):
                password += random.choice(given)
            users.password = password
            users.save()
            context = {
                "user": users
            }
            return render(request, 'forgot-password1.html', context=context)

        else:
            messages.info(request, 'EmailID is not registered')
    return render(request, 'forgot-password.html')


def openview(request, *args, **kwargs):
    return render(request, 'index.html')


def ticket(request, *args, **kwargs):
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        company = request.POST.get('company')
        products = request.POST.get('products')
        Why = request.POST.get('why')
        email = request.POST.get('email')
        gst = request.POST.get('gstin')
        apikey = "64c34bf9719d92d942a2e14be5915c23"
        GSTINNumber = gst
        check = f"http://sheet.gstincheck.co.in/check/{apikey}/{GSTINNumber}"
        result = requests.get(check).json()
        if result['message'] == 'GSTIN  found.':
            send_mail('Retailer Request', f'Name: {firstName} {lastName}\nCompany: {company}\nProducts: {products}\nReason: {Why}\nEmail: {email}\nGST: {gst}',
                      'retailiiti@gmail.com', ['retailiiti@gmail.com'], fail_silently=False)
            return HttpResponse('Your request is sent to the admins.')
        else:
            return HttpResponse('GST IN Not found.')

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
    # username = request.POST.get('Name')
    userlist = User.objects.filter(email=email).values()
    # print(userlist)

    # print("1234567890")

    if len(userlist) > 0:
        userA = userlist[0]
        # if check_password(password, userA['password']):
        if password == userA['password']:
            # print(userA['name'])
            context = {
                "userid": email
            }
            request.session['eid'] = userA['id']
            # return render(request, 'index_mainpage.html', {'userMain': userA['name']})
            return redirect('/main-page/', context=context)
            # return redirect('../home/', {'userMain': userA['name']})

        else:
            messages.info(request, 'Wrong password')
            return redirect('../')

    else:
        messages.info(request, 'User is not registered')
        return redirect('../')


def welcome(request, *args, **kwargs):
    return render(request, 'Welcome.html')
