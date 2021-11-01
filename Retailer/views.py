from django.shortcuts import render,redirect
from django.contrib import messages
from shopapp.models import Product
from login.models import Retailer
# Create your views here.

def mainpage(request, *args, **kwargs):
    rid = request.session.get('rid')
    print(rid)
    product_item = Product.objects.filter(Retailer_ID=rid)
    print(product_item)
    context = {
        "product": product_item,
        # "userid": userid
    }
    return render(request, 'retailer_mainpage.html',context=context)

# def productList(request, *args, **kwargs):
#     list = Product.objects.all()

def add_product_form(request, *args, **kwargs):
    return render(request, 'add-product-form.html')

def update_product_form(request, *args, **kwargs):
    return render(request, 'update-product-form.html')

def add_product(request, *args, **kwargs):
    a = Product()
    a.Retailer_ID = request.session.get('rid')
    a.product_name = request.POST.get('product_name')
    a.price = request.POST.get('price')
    a.company_name = request.POST.get('company_name')
    a.availability = request.POST.get('availability')
    a.image = request.POST.get('image')
    a.save()
    messages.info(request, "New Product added")
    return redirect(request, '/Retailer/')

# def update_product_auth(request, *args, **kwargs):
    
#     P.save()
#     return render(request, 'retailer_mainpage.html')