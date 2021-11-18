from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum
from login.models import User


def initiate_payment(request, id=None, *args, **kwargs):
    eid = request.session.get('eid')
    get_user = User.objects.filter(id=eid).values()
    user = get_user[0]['name']
    amount = request.POST['pay_product']
    if request.method == "POST":
        context = {
            "user": user,
            "amount": amount,
            "id": id
        }
        return render(request, 'payments/pay.html', context=context)


def cart_initiate_payment(request, id=None, *args, **kwargs):
    eid = request.session.get('eid')
    get_user = User.objects.filter(id=eid).values()
    user = get_user[0]['name']
    amount = request.POST['pay_product']
    if request.method == "POST":
        context = {
            "user": user,
            "amount": amount,
            "id": id
        }
        return render(request, 'payments/cart_pay.html', context=context)

def cartall_initiate_payment(request, id=None, *args, **kwargs):
    eid = request.session.get('eid')
    get_user = User.objects.filter(id=eid).values()
    user = get_user[0]['name']
    amount = request.POST['pay_product']
    if request.method == "POST":
        context = {
            "user": user,
            "amount": amount,
            "id": id
        }
        return render(request, 'payments/cartall_pay.html', context=context)


def proceed_payment(request, id=None, *args, **kwargs):
    if request.method == "POST":
        eid = request.session.get('eid')
        get_user = User.objects.filter(id=eid).values()
        user = get_user[0]['name']
        amount = request.POST['proceed_product']

        transaction = Transaction.objects.create(made_by_id=eid, amount=amount)
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY

        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(transaction.made_by.email)),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        return render(request, 'payments/redirect.html', context=paytm_params)


def cart_proceed_payment(request, id=None, *args, **kwargs):
    if request.method == "POST":
        eid = request.session.get('eid')
        get_user = User.objects.filter(id=eid).values()
        user = get_user[0]['name']
        amount = request.POST['proceed_product']

        transaction = Transaction.objects.create(made_by_id=eid, amount=amount)
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY

        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(transaction.made_by.email)),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        return render(request, 'payments/redirect.html', context=paytm_params)

def cartall_proceed_payment(request, id=None, *args, **kwargs):
    if request.method == "POST":
        eid = request.session.get('eid')
        get_user = User.objects.filter(id=eid).values()
        user = get_user[0]['name']
        amount = request.POST['proceed_product']

        transaction = Transaction.objects.create(made_by_id=eid, amount=amount)
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY

        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(transaction.made_by.email)),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        return render(request, 'payments/redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(
            paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'payments/callback.html', context=received_data)
        return render(request, 'payments/callback.html', context=received_data)
