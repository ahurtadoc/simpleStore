import httpx
from base64 import b64encode
from hashlib import sha1
from datetime import datetime, timedelta
from os import urandom
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST

from .forms import buyerForm
from .models import Orders


# Views

def index(request):
    orders = get_list_or_404(Orders)  # get all orders from db
    return render(request, 'store/index.html', {'orders': orders, 'code': None})


def buy(request):
    """
    Django forms manipulate to redirect to order resume
    Other wise  show the blank form
    """
    if request.method == 'POST':
        form = buyerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            mobile = form.cleaned_data['mobile']
            order = Orders(customer_name=name, customer_email=email, customer_mobile=mobile, status='CREATED')
            order.save()
            return HttpResponseRedirect('buy/' + str(order.id))
        else:
            return HttpResponse('error')
    else:
        form = buyerForm()
        return render(request, 'store/buy.html', {'form': form})


def resume(request, order_id):
    """
    Redirect to function that create request to payment gateway or
    if payment once tried redirect to order state view
    """
    if request.method == 'POST':
        return HttpResponseRedirect(request, '../pay/' + order_id)
    else:
        order = get_object_or_404(Orders, pk=order_id)
        if order.session_id:
            return HttpResponseRedirect('../state/' + str(order_id))
        else:
            return render(request, 'store/resume.html', {'order': order})


@require_POST
def pay(request, order_id):
    """
    Create a payment request and redirect to payment gateway process url
    """
    order = get_object_or_404(Orders, pk=order_id)
    expirationDate = datetime.now() + timedelta(hours=12)
    auth = auth_data()
    dataRequest = {
        'auth': auth,
        'payment': {
            "reference": order.id,
            "description": "Payment single product",
            "amount": {
                "currency": "COP",
                "total": "50000"
            }
        },
        "locale": "es_CO",
        "buyer": {
            "name": order.customer_name.split()[0],
            "email": order.customer_email,
            "mobile": order.customer_mobile
        },
        "expiration": expirationDate.isoformat(),
        "returnUrl": "http://localhost:8000/store/state/" + str(order.id),
        "ipAddress": "127.0.0.1",
        "userAgent": "PlacetoPay Sandbox"
    }
    headers = {'Content-Type': 'application/json'}
    url = 'https://test.placetopay.com/redirection/api/session/'
    payRequest = httpx.post(url, headers=headers, json=dataRequest)
    dataPayRequest = payRequest.json()
    order.session_id = str(dataPayRequest['requestId'])
    order.process_url = dataPayRequest['processUrl']
    order.save()
    return HttpResponseRedirect(dataPayRequest['processUrl'])


def order_state(request, order_id):
    """
    Get information about payment status and change model status
    to specify if order is payed or could be try to pay it
    """
    order = get_object_or_404(Orders, pk=order_id)
    if request.method == 'POST':
        return HttpResponseRedirect(order.process_url)
    else:
        if order.status != 'PAYED':
            headers = {'Content-Type': 'application/json'}
            data = {'auth': auth_data()}
            url = 'https://test.placetopay.com/redirection/api/session/' + order.session_id
            stateRequest = httpx.post(url, headers=headers, json=data)
            statePayRequest = stateRequest.json()
            status = statePayRequest['status']['status']
            if status == 'APPROVED':
                order.status = 'PAYED'
            elif status == 'REJECTED':
                order.status = 'REJECTED'
            else:
                order.status = 'CREATED'
            order.save()
        return render(request, 'store/state.html', {'order': order})


# Helpers
def auth_data():
    """
    Generate auth data to payment gateway
    """
    nonce = hex(int.from_bytes(urandom(16), byteorder="big")).encode('utf8')
    seed = datetime.now().isoformat().encode('utf8')  # Current date in iso format
    secret_key = '024h1IlD'.encode('utf8')
    trankey = sha1(nonce + seed + secret_key).digest()  # to use sha1, parameters need to encode in utf8
    data = {
        'login': '6dd490faf9cb87a9862245da41170ff2',
        'seed': seed.decode('utf8'),
        'tranKey': b64encode(trankey).decode('utf8'),
        'nonce': b64encode(nonce).decode('utf8')
    }
    return data
