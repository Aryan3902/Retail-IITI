from django.shortcuts import render

from django.contrib import messages
from django.http.response import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from login.models import User
from .models import Product, Cart, CartItem



def main_page(request, *args, **kwargs):
    product_item = Product.objects.all()
    context = {
        "product": product_item,
        # "userid": userid
    }
    return render(request, 'index_mainpage.html', context=context)

def cart(request, *args, **kwargs):
    eid = request.session.get('eid')
    product_item = CartItem.objects.filter(user_id=eid)
    context = {
        "product": product_item,
        "id": eid
    }
    return render(request, 'cart.html', context=context)