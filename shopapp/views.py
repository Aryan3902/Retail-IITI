from django.shortcuts import render
from django.core import mail
from django.conf import settings
from django.core.mail import send_mail

from django.contrib import messages
from django.http.response import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from login.models import User
from .models import Product, Cart, CartItem, Orders



def main_page(request, *args, **kwargs):

    if 'search' in request.POST:
        query = request.POST.get('search')
        try:
            int(query)
            check = True
        except:
            check = False
        if check:
            product_item = Product.objects.filter(product_id=query).values()
            context = {
                "product": product_item
                # "userid": userid
            }
            return render(request, 'index_mainpage.html', context=context)

        else:
            product_item1 = Product.objects.filter(product_name=query).values()
            # product_item1 = Product.objects.filter(query in product_name).values()
            product_item2 = Product.objects.filter(company_name=query).values()
            product_item3 = Product.objects.filter(availability=query).values()
            if len(product_item1)>0:
                context = {
                "product": product_item1,
                # "userid": userid
                }
                return render(request, 'index_mainpage.html', context=context)
            
            elif len(product_item2)>0:
                context = {
                "product": product_item2,
                # "userid": userid
                }
                return render(request, 'index_mainpage.html', context=context)
            
            else:
                context = {
                "product": product_item3,
                # "userid": userid
                }
                return render(request, 'index_mainpage.html', context=context)

            
    product_item = Product.objects.all()
    context = {
        "product": product_item,
        # "userid": userid
    }
    return render(request, 'index_mainpage.html', context=context)


def cart(request, *args, **kwargs):
    id = None
    eid = request.session.get('eid')

    if 'search' in request.POST:
        query = request.POST.get('search')
        try:
            int(query)
            check = True
        except:
            check = False
        if check:
            product_item = CartItem.objects.filter(product_id=query, user_id=eid)
            context = {
                "product": product_item
                # "userid": userid
            }
            return render(request, 'cart.html', context=context)

        else:
            return render(request, 'cart.html')


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

    if 'search' in request.POST:
        query = request.POST.get('search')
        try:
            int(query)
            check = True
        except:
            check = False
        if check:
            product_item = Orders.objects.filter(product_id=query, user_id=eid)
            context = {
                "product": product_item
                # "userid": userid
            }
            return render(request, 'orders.html', context=context)

        else:
            return render(request, 'orders.html')

    if 'order' in request.POST:
        id = request.POST.get('order')

        user_list = User.objects.filter(id=eid).values()
        user1 = user_list[0]
        user = user1['name']
        product_list = Product.objects.filter(product_id=id).values()
        product1 = product_list[0]
        product = product1['product_name']
        price_ht = product1['price']
        company = product1['company_name']

        list = Orders()
        list.product_id = id
        # list.cart_id = 1
        list.price_ht = price_ht
        list.user_id = eid
        list.save()

        order2 = Orders.objects.all().last()

        email = User.objects.filter(id=eid)
        email1 = email[0]
        email2 = email1.email
        user2 = email1.name
        # send_mail('Order Placed', 'rerhthhr',
        #     'retailiiti@gmail.com', [eid], fail_silently=False)

        # with mail.get_connection() as connection:
        #     mail.EmailMessage(
        #         eid, eid, 'retailiiti@gmail.com', ['cse200001043@iiti.ac.in'],
        #         connection=connection,
        #     ).send()
        subject = 'Order Placed'
        message =f'''
        Hi {user2}, your order has been placed. 

        Order Details: 

        Order Id: { order2.id }
        Product Id: { id }
        Product Name: { product }
        Company Name: { company }
        '''
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email2, ]
        send_mail( subject, message, email_from, recipient_list )

        delete_all = CartItem.objects.filter(user_id=eid, product_id=id).delete()


    if 'cancel' in request.POST:
        id = request.POST.get('cancel')

        user_list = User.objects.filter(id=eid).values()
        user1 = user_list[0]
        user = user1['name']

        order_to = Orders.objects.filter(id=id).values()
        order2 = order_to[0]
        product_id = order2['product_id']
        product_to_cancel = Product.objects.filter(product_id=product_id).values()
        product12 = product_to_cancel[0]
        final_list = Orders.objects.filter(id=id).delete()
    #     # final_list1 = final_list

        email = User.objects.filter(id=eid)
        email1 = email[0]
        email2 = email1.email
        user2 = email1.name

        subject = 'Order Cancelled'
        message =f'''
        Hi {user2}, your order has been cancelled. 

        Order Details: 
        
        Order Id: { order2['id'] }
        Product Id: { product_id }
        Product Name: { product12['product_name'] }
        Company Name: { product12['company_name'] }
        '''
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email2, ]
        send_mail( subject, message, email_from, recipient_list )


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
        total_order = ''''''
        for x in range(len(list1)):
            abc = list1[x]
            abcd = abc['id']
            cart_item = CartItem.objects.filter(id=abcd).values()
            cart_item1 = cart_item[0]
            id1 = cart_item1['product_id']
            price_ht = cart_item1['price_ht']
            product_find = Product.objects.filter(product_id=id1).values()
            product_find1 = product_find[0]
            name_product = product_find1['product_name']
            company = product_find1['company_name']

            list = Orders()
            list.product_id = id1
            # list.cart_id = 1
            list.price_ht = price_ht
            list.user_id = eid
            list.save()

            order2 = Orders.objects.all().last()

            total_order += f'''
            { x+1 }. Order Id: { order2.id }
                Product Id: { id1 }
                Product Name: { name_product }
                Company Name: { company }
            '''
        
        email = User.objects.filter(id=eid)
        email1 = email[0]
        email2 = email1.email
        user2 = email1.name

        subject = 'Order Placed'
        message =f'''
        Hi {user2}, your order has been placed. 

        Order Details: 
        { total_order }
        '''
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email2, ]
        send_mail( subject, message, email_from, recipient_list )

        delete_all = CartItem.objects.filter(user_id=eid).delete()


    product_item = Orders.objects.filter(user_id=eid)

    context = {
        "product": product_item,
        # "id": id,
        "eid":eid
    }
    return render(request, 'orders.html', context=context)