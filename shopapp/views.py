from django.shortcuts import render

from django.contrib import messages
from django.http.response import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from .models import Product



def main_page(request, *args, **kwargs):
    product_item = Product.objects.all()
    context = {
        "product": product_item
    }
    return render(request, 'index_mainpage.html', context=context)