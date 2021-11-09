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
    eid = request.session.get('eid')
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
            if len(product_item1) > 0:
                context = {
                    "product": product_item1,
                    # "userid": userid
                }
                return render(request, 'index_mainpage.html', context=context)

            elif len(product_item2) > 0:
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
    username = User.objects.filter(id=eid)
    user = username[0]
    context = {
        "product": product_item,
        'user': user
        # "userid": userid
    }
    return render(request, 'index_mainpage.html', context=context)



def main_page_electronics(request, *args, **kwargs):

            
    product_item = Product.objects.filter(category="Electronics")
    context = {
        "product": product_item,
        # "userid": userid
    }
    return render(request, 'category_electronics.html', context=context)


def main_page_stationary(request, *args, **kwargs):

            
    product_item = Product.objects.filter(category="Stationary")
    context = {
        "product": product_item,
        # "userid": userid
    }
    return render(request, 'category_stationary.html', context=context)


def main_page_household(request, *args, **kwargs):

            
    product_item = Product.objects.filter(category="Household")
    context = {
        "product": product_item,
        # "userid": userid
    }
    return render(request, 'category_household.html', context=context)


def main_page_fashion(request, *args, **kwargs):

            
    product_item = Product.objects.filter(category="Fashion")
    context = {
        "product": product_item,
        # "userid": userid
    }
    return render(request, 'category_fashion.html', context=context)


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
            product_item = CartItem.objects.filter(
                product_id=query, user_id=eid)
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

        cart = Cart.objects.last()
        cart_id = cart.id

        if len(final_list) == 0:

            list = CartItem()
            list.product_id = id
            list.cart_id = cart_id
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

        final_list = CartItem.objects.filter(
            product_id=id, user_id=eid).delete()

    product_item = CartItem.objects.filter(user_id=eid)
    # cart1 = product_item[0]
    total_price = 0
    for x in product_item:
        total_price += x.product.price
    username = User.objects.filter(id=eid)
    user = username[0]
    context = {
        "product": product_item,
        "id": id,
        "eid": eid,
        "total": total_price,
        "user": user
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
    eid = request.session.get('eid')
    if 'quantity' in request.POST:
        value = request.POST.get('quantity')
        product_item1 = Product.objects.filter(product_id=id).values()
        product1 = product_item1[0]
        product_item2 = product1['price']
        cart = CartItem.objects.get(user_id=eid, product_id=id)
        # product_item = CartItem.objects.filter(user_id=eid, product_id=id)
        product_item = CartItem.objects.filter(user_id=eid, product_id=id)

        # cart_id = cart['id']
        cart.quantity = value
        cart.price_ht = int(product_item2) * int(value)
        cart.save()

        context = {
            "product": product_item,
            "cart_quantity": cart.quantity,
            "price": cart.price_ht
            # "userid": userid
        }
        return render(request, 'index_itempage1.html', context=context)

    if id is not None:
        product_item1 = Product.objects.filter(product_id=id)
        cart = CartItem.objects.filter(user_id=eid, product_id=id).values()
        cart_id = cart[0]['id']
        cart_quantity = cart[0]['quantity']
        product_item = CartItem.objects.filter(user_id=eid, product_id=id)

        context = {
            "product": product_item,
            "cart_quantity": cart_quantity
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


    if 'order1' in request.POST:
        id = request.POST.get('order1')

        user_list = User.objects.filter(id=eid).values()
        user1 = user_list[0]
        user = user1['name']
        product_list = Product.objects.filter(product_id=id).values()
        product1 = product_list[0]
        product = product1['product_name']
        
        company = product1['company_name']
        
        price_ht = product1['price']

        list = Orders()
        list.product_id = id
        # list.cart_id = 1
        list.quantity = 1
        list.price_ht = price_ht
        list.user_id = eid
        list.save()

        order2 = Orders.objects.all().last()

        email = User.objects.filter(id=eid)
        email1 = email[0]
        email2 = email1.email
        user2 = email1.name

        subject = 'Order Placed'
        message = f'''
        Hi {user2}, your order has been placed. 

        Order Details: 

        Order Id: { order2.id }
        Product Id: { id }
        Product Name: { product }
        Company Name: { company }
        Quantity: 1
        '''
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email2, ]
        send_mail(subject, message, email_from, recipient_list)





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
        # price_ht = product1['price']
        company = product1['company_name']
        Cart = CartItem.objects.filter(user_id=eid, product_id=id).values()
        cart = Cart[0]
        quantity = cart['quantity']
        price_ht = cart['price_ht']

        list = Orders()
        list.product_id = id
        # list.cart_id = 1
        list.quantity = quantity
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
        message = f'''
        Hi {user2}, your order has been placed. 

        Order Details: 

        Order Id: { order2.id }
        Product Id: { id }
        Product Name: { product }
        Company Name: { company }
        Quantity: { quantity }
        '''
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email2, ]
        send_mail(subject, message, email_from, recipient_list)

        delete_all = CartItem.objects.filter(
            user_id=eid, product_id=id).delete()

    if 'cancel' in request.POST:
        id = request.POST.get('cancel')

        user_list = User.objects.filter(id=eid).values()
        user1 = user_list[0]
        user = user1['name']

        order_to = Orders.objects.filter(id=id).values()
        order2 = order_to[0]
        product_id = order2['product_id']
        product_to_cancel = Product.objects.filter(
            product_id=product_id).values()
        product12 = product_to_cancel[0]
        final_list = Orders.objects.filter(id=id).delete()
    #     # final_list1 = final_list

        email = User.objects.filter(id=eid)
        email1 = email[0]
        email2 = email1.email
        user2 = email1.name

        subject = 'Order Cancelled'
        message = f'''
        Hi {user2}, your order has been cancelled. 

        Order Details: 
        
        Order Id: { order2['id'] }
        Product Id: { product_id }
        Product Name: { product12['product_name'] }
        Company Name: { product12['company_name'] }
        '''
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email2, ]
        send_mail(subject, message, email_from, recipient_list)

        product_item = Orders.objects.filter(user_id=eid)
        # # cart1 = product_item[0]
        # total_price = 0
        # for x in product_item:
        #     total_price += x.product.price
        context = {
            "product": product_item,
            "eid": eid,
            "id": id
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
            quantity123 = cart_item['quantity']
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
                Quantity: { quantity123 }
            '''

        email = User.objects.filter(id=eid)
        email1 = email[0]
        email2 = email1.email
        user2 = email1.name

        subject = 'Order Placed'
        message = f'''
        Hi {user2}, your order has been placed. 

        Order Details: 
        { total_order }
        '''
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email2, ]
        send_mail(subject, message, email_from, recipient_list)

        delete_all = CartItem.objects.filter(user_id=eid).delete()

    product_item = Orders.objects.filter(user_id=eid)

    context = {
        "product": product_item,
        # "id": id,
        "eid": eid
    }
    return render(request, 'orders.html', context=context)


def aboutus(request):
    return render(request, 'index_aboutus.html')


def profile(request, id=None, *args, **kwargs):

    eid = request.session.get('eid')

    form_name = None
    form_email = None
    form_password = None
    form_new_password = None
    form_confirm_password = None
    form_gender = None
    form_hostel = None
    form_room = None
    form_phone = None

    if 'save' in request.POST:
        form_name = request.POST.get('name')
        form_email = request.POST.get('email')
        form_password = request.POST.get('password')
        form_new_password = request.POST.get('new-password')
        form_confirm_password = request.POST.get('confirm-password')
        form_gender = request.POST.get('gender')
        form_hostel = request.POST.get('hostel')
        form_room = request.POST.get('room')
        form_phone = request.POST.get('phone')

        edit_user = User.objects.get(id=eid)

        if form_name:
            edit_user.name = form_name

        if form_email:
            if len(User.objects.filter(email=form_email))>0:
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

        if form_gender:
            edit_user.gender = form_gender

        if form_hostel:
            edit_user.hostel = form_hostel

        if form_room:
            edit_user.room = form_room

        if form_phone:
            edit_user.phone = form_phone

        
        edit_user.save()


    user_list = User.objects.filter(id=eid).values()
    room = None
    phone = None
    gender = None
    hostel1 = None
    hostel2 = None
    hostel3 = None
    hostel4 = None
    hostel5 = None

    if user_list[0]['phone']!='None':
        phone = user_list[0]['phone']
    if user_list[0]['room']!='None':
        room = user_list[0]['room']
    if user_list[0]['gender']=='Female':
        gender = user_list[0]['gender']
    if user_list[0]['hostel']=='A. P. J ABDUL KALAM':
        hostel1 = user_list[0]['hostel']
    if user_list[0]['hostel']=='HOMI JEHANGIR BHABHA':
        hostel2 = user_list[0]['hostel']
    if user_list[0]['hostel']=='VIKRAM SARABHAI':
        hostel3 = user_list[0]['hostel']
    if user_list[0]['hostel']=='DEVI AHILYA':
        hostel4 = user_list[0]['hostel']
    if user_list[0]['hostel']=='C. V. RAMAN':
        hostel5 = user_list[0]['hostel']


    context = {
    "name": user_list[0]['name'],
    "email": user_list[0]['email'],
    "room": room,
    "phone": phone,
    "gender": gender,
    "hostel1": hostel1,
    "hostel2": hostel2,
    "hostel3": hostel3,
    "hostel4": hostel4,
    "hostel5": hostel5
    }
    return render(request, 'student_profile.html', context=context)