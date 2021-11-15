from django.shortcuts import render,redirect
from django.contrib import messages
from login.models import User, Retailer
from shopapp.models import Product, Cart, CartItem, Orders, Wishlist
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.

def mainpage(request, *args, **kwargs):
    try:
        re=request.META['HTTP_REFERER']
    except:
        re ="None"
    # print(re)
    if(not("http://127.0.0.1:8000/" in re)):
        return redirect("../")
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
    a.category = request.POST.get('category')
    a.availability=request.POST.get('availability')
    a.company_name = request.POST.get('company_name')
    a.image = request.POST.get('image')
    a.save()
    messages.info(request, "New Product added")
    return redirect('/Retailer/')

def update_product(request, *args, **kwargs):
    Id=request.session.get('pid')
    a = Product.objects.get(product_id=Id)
    print(request.POST.get('company_name'))
    if (request.POST.get('product_name')!=''):
        a.product_name = request.POST.get('product_name')
    if (request.POST.get('price')!=''):
        a.price = request.POST.get('price')
    if (request.POST.get('company_name')!=''):
        a.company_name = request.POST.get('company_name')
    if (request.POST.get('category')!=''):
        a.category = request.POST.get('category')
        print(a.category)
    if (request.POST.get('availability')!=''):
        a.availability = request.POST.get('availability')
    if (request.POST.get('image')!=''):
        a.image = request.POST.get('image')
    a.save()
    return redirect('/Retailer/')

def delete_product(request, *args, **kwargs):
    Id = request.POST.get('id')
    a = Product.objects.get(product_id=Id)
    a.delete()
    return redirect('/Retailer/')



def retailer_profile(request, id=None, *args, **kwargs):

    eid = request.session.get('rid')

    form_fname = None
    form_lname = None
    form_email = None
    form_password = None
    form_new_password = None
    form_confirm_password = None
    form_company = None
    form_gstno = None
    form_products = None
    form_address = None
    form_city = None
    form_state = None
    form_phone = None

    if 'save' in request.POST:
        form_fname = request.POST.get('fname')
        form_lname = request.POST.get('lname')
        form_email = request.POST.get('email')
        form_password = request.POST.get('password')
        form_new_password = request.POST.get('new-password')
        form_confirm_password = request.POST.get('confirm-password')
        form_company = request.POST.get('company')
        form_gstno = request.POST.get('gstno')
        form_products = request.POST.get('products')
        form_address = request.POST.get('address')
        form_city = request.POST.get('city')
        form_state = request.POST.get('state')
        form_phone = request.POST.get('phone')

        edit_user = Retailer.objects.get(Retailer_ID=eid)

        if form_fname:
            edit_user.first_name = form_fname

        if form_lname:
            edit_user.last_name = form_lname

        if form_email:
            if len(Retailer.objects.filter(email=form_email))>0:
                messages.info(request, 'UserId already registered')
            else:
                if check_password(form_password, edit_user.password):
                    edit_user.email = form_email
                else:
                    if form_password:
                        messages.info(request, 'Incorrect Password')
                    else:
                        messages.info(request, 'Enter your Password')

        if form_new_password:
            if form_new_password == form_confirm_password:
                P = make_password(form_new_password)
                edit_user.password = P
            else:
                messages.info(request, "Password doesn't match")

        if form_company:
            edit_user.company_name = form_company

        if form_gstno:
            edit_user.gstNo = form_gstno

        if form_products:
            edit_user.Products = form_products

        if form_address:
            edit_user.address = form_address

        if form_city:
            edit_user.city = form_city

        if form_state:
            edit_user.state = form_state
    
        if form_phone:
            edit_user.phone = form_phone

        
        edit_user.save()


    user_list = Retailer.objects.filter(Retailer_ID=eid).values()
    phone = None
    address = None
    city = None
    state = None

    if user_list[0]['phone']!='None':
        phone = user_list[0]['phone']
    if user_list[0]['address']!='None':
        address = user_list[0]['address']
    if user_list[0]['city']!='None':
        city = user_list[0]['city']
    if user_list[0]['state']!='None':
        state = user_list[0]['state']


    context = {
    "id": eid,
    "user": user_list[0]['email'],
    "fname": user_list[0]['first_name'],
    "lname": user_list[0]['last_name'],
    "email": user_list[0]['email'],
    "company": user_list[0]['company_name'],
    "gstno": user_list[0]['gstNo'],
    "products": user_list[0]['Products'],
    "phone": phone,
    "address": address,
    "city": city,
    "state": state,
    }
    return render(request, 'retailer_profile.html', context=context)

def retailer_orders(request, *args, **kwargs):
    eid = request.session.get('rid')

    product_item = Orders.objects.filter(Retailer_ID_id=eid)

    context = {
        "product": product_item,
        # "id": id,
    }
    return render(request, 'retailer_orders.html', context=context)


def retailer_orders_product(request, id=None, *args, **kwargs):
    # article_obj = None
    if'status' in request.POST:
        status = request.POST.get('status')
        edit_order = Orders.objects.get(id=id)
        edit_order.Status = status
        edit_order.save()

    if id is not None:
        # product_item = Product.objects.filter(product_id=id)
        order_item = Orders.objects.filter(id=id)
        order12 = order_item[0]
        context = {
            "product": order_item,
            "order": order12
            # "userid": userid
        }
        return render(request, 'retailer_itempage.html', context=context)