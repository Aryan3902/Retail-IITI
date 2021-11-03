from django.contrib import messages
from django.core import mail
from django.conf import settings
from django.core.mail import send_mail
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from .models import User,Retailer
import random

# Create your views here.


def homeview(request, *args, **kwargs):
    return render(request, 'login-register.html')


def forgetview(request, *args, **kwargs):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        
        userlist = User.objects.filter(name=name, email=email).values()

        if len(userlist)>0:
            users = User.objects.get(email=email)

            password = ""
            given="QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuioplkjhgfdsazxcvbnm1234567890"
            for x in range(10):
                password += random.choice(given)
            users.password = make_password(password)
            users.save()
            context = {
                "user": password
            }
            return render(request, 'forgot-password1.html', context=context)
        
        else:
            messages.info(request, 'EmailID is not registered')
    return render(request, 'forgot-password.html')



def openview(request, *args, **kwargs):
    return render(request, 'index.html')


def ticket(request, *args, **kwargs):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        company_name = request.POST.get('company')
        products = request.POST.get('products')
        why_you = request.POST.get('why')
        email = request.POST.get('email')
        gst_no = request.POST.get('gstin')

        # send_mail('Retailer Request', 'LET ME INNNNNNNNNNNNNN',
        #           'retailiiti@gmail.com', ['retailiiti@gmail.com'], fail_silently=False)
        # return HttpResponse('Your request is sent to the admins.')
        subject = 'Retailer Request'
        message =f'''
        Hi , there is a retailer waiting for a response. 

        Retailer Info: 

        Name:  { first_name } { last_name }
        Company Name: { company_name }
        Products: { products }
        Why You: { why_you }
        Email: { email }
        GST No.: { gst_no }
        '''
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['retailiiti@gmail.com', ]
        send_mail( subject, message, email_from, recipient_list )

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
    # username = request.POST.get('Name')
    userlist = User.objects.filter(email=email).values()
    # print(userlist)
    
    # print("1234567890")

    if len(userlist)>0:
        userA = userlist[0]
        if check_password(password, userA['password']):
        # if password == userA['password']:
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


def relogin(request, *args, **kwargs):
    email = request.POST.get('email')
    password = request.POST.get('password')
    # username = request.POST.get('Name')
    userlist = Retailer.objects.filter(email=email).values()
    # print(userlist)
    
    # print("1234567890")

    if len(userlist)>0:
        userA = userlist[0]
        if check_password(password, userA['password']):
        # if password == userA['password']:
            # print(userA['name'])
            context = {
                "userid": email
            }
            request.session['rid'] = userA['Retailer_ID']
            # return render(request, 'index_mainpage.html', {'userMain': userA['name']})
            return redirect('/Retailer', context=context)
            # return redirect('../home/', {'userMain': userA['name']})

        else:
            messages.info(request, 'Wrong password')
            return redirect('../')

    else:
        messages.info(request, 'Retailer is not registered')
        return redirect('../')


def welcome(request, *args, **kwargs):
    return render(request, 'Welcome.html')

