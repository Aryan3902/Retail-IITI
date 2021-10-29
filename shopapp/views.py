from django.shortcuts import render

from django.contrib import messages
from django.http.response import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from login.models import User
from .models import Product, Cart, CartItem, Orders



def main_page(request, *args, **kwargs):
    product_item = Product.objects.all()
    context = {
        "product": product_item,
        # "userid": userid
    }
    return render(request, 'index_mainpage.html', context=context)


def cart(request, *args, **kwargs):
    id = None
    eid = request.session.get('eid')
    if 'name' in request.POST:
        id = request.POST.get('name')

        user_list = User.objects.filter(id=eid).values()
        user1 = user_list[0]
        user = user1['name']
        product_list = Product.objects.filter(product_id=id).values()
        product1 = product_list[0]
        product = product1['product_name']
        price_ht = product1['price']

        final_list = CartItem.objects.filter(product_id=id, user_id=eid)
        final_list1 = final_list

        if len(final_list)==0:

            list = CartItem()
            list.product_id = id
            list.cart_id = 1
            list.price_ht = price_ht
            list.user_id = eid
            list.save()



    if 'remove' in request.POST:
        id = request.POST.get('remove')

        user_list = User.objects.filter(id=eid).values()
        user1 = user_list[0]
        user = user1['name']
        product_list = Product.objects.filter(product_id=id).values()
        product1 = product_list[0]
        product = product1['product_name']

        final_list = CartItem.objects.filter(product_id=id, user_id=eid).delete()
   

    product_item = CartItem.objects.filter(user_id=eid)
    # cart1 = product_item[0]
    total_price = 0
    for x in product_item:
        total_price += x.product.price


    context = {
        "product": product_item,
        "id": id,
        "eid":eid,
        "total": total_price
        # "cart": cart1
    }
    return render(request, 'cart.html', context=context)




def main_page_product(request, id=None, *args, **kwargs):
    # article_obj = None
    if id is not None:
        product_item = Product.objects.filter(product_id=id)
        context = {
            "product": product_item
            # "userid": userid
        }
        return render(request, 'index_itempage.html', context=context)


def main_page_cart_product(request, id=None, *args, **kwargs):
    # article_obj = None
    if id is not None:
        product_item = Product.objects.filter(product_id=id)
        context = {
            "product": product_item
            # "userid": userid
        }
        return render(request, 'index_itempage1.html', context=context)

def main_page_order_product(request, id=None, *args, **kwargs):
    # article_obj = None
    if id is not None:
        # product_item = Product.objects.filter(product_id=id)
        order_item = Orders.objects.filter(id=id)
        order12 = order_item[0]
        context = {
            "product": order_item,
            "order": order12
            # "userid": userid
        }
        return render(request, 'index_itempage2.html', context=context)


def orders(request, *args, **kwargs):
    id = None
    eid = request.session.get('eid')
    if 'order' in request.POST:
        id = request.POST.get('order')

        user_list = User.objects.filter(id=eid).values()
        user1 = user_list[0]
        user = user1['name']
        product_list = Product.objects.filter(product_id=id).values()
        product1 = product_list[0]
        product = product1['product_name']
        price_ht = product1['price']

        list = Orders()
        list.product_id = id
        # list.cart_id = 1
        list.price_ht = price_ht
        list.user_id = eid
        list.save()

    if 'cancel' in request.POST:
        id = request.POST.get('cancel')

        user_list = User.objects.filter(id=eid).values()
        user1 = user_list[0]
        user = user1['name']

        final_list = Orders.objects.filter(id=id).delete()
    #     # final_list1 = final_list


        product_item = Orders.objects.filter(user_id=eid)
        # # cart1 = product_item[0]
        # total_price = 0
        # for x in product_item:
        #     total_price += x.product.price
        context = {
            "product": product_item,
            "eid":eid,
            "id":id
        }
        return render(request, 'orders.html', context=context)

    
    if 'buyall' in request.POST:
        list1 = CartItem.objects.filter(user_id=eid).values()
        
        user_list = User.objects.filter(id=eid).values()
        user1 = user_list[0]
        user = user1['name']
        for x in range(len(list1)):
            abc = list1[x]
            abcd = abc['id']
            cart_item = CartItem.objects.filter(id=abcd).values()
            cart_item1 = cart_item[0]
            id1 = cart_item1['product_id']
            price_ht = cart_item1['price_ht']

            list = Orders()
            list.product_id = id1
            # list.cart_id = 1
            list.price_ht = price_ht
            list.user_id = eid
            list.save()


    product_item = Orders.objects.filter(user_id=eid)

    context = {
        "product": product_item,
        # "id": id,
        "eid":eid
    }
    return render(request, 'orders.html', context=context)