from django.shortcuts import render,redirect
from django.contrib import messages
from shopapp.models import Product
from login.models import Retailer
from django.http import HttpResponse
# Create your views here.

def mainpage(request, *args, **kwargs):
    rid = request.session.get('rid')
    # print(rid)
    product_item = Product.objects.filter(Retailer_ID=rid)
    # print(product_item)
    context = {
        "product": product_item,
        # "userid": userid
    }
    return render(request, 'retailer_mainpage.html',context=context)

# def productList(request, *args, **kwargs):
#     list = Product.objects.all()

def add_product_form(request, *args, **kwargs):
    return render(request, 'add-form.html')

def update_product_form(request, *args, **kwargs):
    Id = request.POST.get('id')
    product_item = Product.objects.get(product_id=Id)
    context = {
        "x": product_item,
    }
    request.session['pid'] = Id
    return render(request, 'update-form.html',context=context)
    # return HttpResponse("<h1>Hello</h1>")

def add_product(request, *args, **kwargs):
    a = Product()
    Id = request.session.get('rid')
    userlist = Retailer.objects.filter(Retailer_ID=Id)
    a.Retailer_ID = userlist[0]
    a.product_name = request.POST.get('product_name')
    a.price = request.POST.get('price')
    a.company_name = request.POST.get('company_name')
    a.Quantity = request.POST.get('availability')
    a.image = request.POST.get('image')
    a.save()
    messages.info(request, "New Product added")
    return redirect('/Retailer/')

def update_product(request, *args, **kwargs):
    Id=request.session.get('pid')
    a = Product.objects.get(product_id=Id)
    if (request.POST.get('product_name')!=''):
        a.product_name = request.POST.get('product_name')
    if (request.POST.get('price')!=''):
        a.price = request.POST.get('price')
    if (request.POST.get('company_name')!=''):
        a.company_name = request.POST.get('company_name')
    if (request.POST.get('availability')!=''):
        a.Quantity = request.POST.get('availability')
    if (request.POST.get('image')!=''):
        a.image = request.POST.get('image')
    a.save()
    return redirect('/Retailer/')

def delete_product(request, *args, **kwargs):
    Id = request.POST.get('id')
    a = Product.objects.get(product_id=Id)
    a.delete()
    return redirect('/Retailer/')