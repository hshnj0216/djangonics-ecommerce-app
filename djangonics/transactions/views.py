from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Order, OrderItem
from django.shortcuts import render, redirect, reverse
import json
import requests
import sys
from django.http import JsonResponse
from accounts.models import Address
from products.models import CartItem

# Create your views here.

client_id = 'ATq1dwh2EUeN17EwoFcOdVylRg8jJAIt_9yDXDt83oO2EE2vwc8uUC-5LPcn6-7gPKsOVR0PjKjZG4x_'
client_secret = 'ECe8YLL6r3g0D57lwc7-s4CPh2EVgWNlxEdn81K8vizlEENGJh9MF-hK0DfLeUTkILV3FlK-5AElab6V'


@login_required
def authorize_payment(request):
    print('authorize_payment')

    # Get an access token
    auth_response = requests.post(
        'https://api.sandbox.paypal.com/v1/oauth2/token',
        auth=(client_id, client_secret),
        headers={'Accept': 'application/json'},
        data={'grant_type': 'client_credentials'}
    )
    access_token = auth_response.json()['access_token']

    # Set the order ID
    order_id = request.POST.get('order_id')

    # Authorize the payment
    authorize_response = requests.post(
        f'https://api.sandbox.paypal.com/v2/checkout/orders/{order_id}/authorize',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
    )

    authorization = authorize_response.json()

    return JsonResponse(authorization)


@login_required
def capture_payment(request):
    # Get an access token
    auth_response = requests.post(
        'https://api.sandbox.paypal.com/v1/oauth2/token',
        auth=(client_id, client_secret),
        headers={'Accept': 'application/json'},
        data={'grant_type': 'client_credentials'}
    )
    access_token = auth_response.json()['access_token']

    # Get authorization id
    authorization_id = request.POST.get('authorization_id')

    # Set capture amount
    order_amount = request.POST.get('order_amount')
    capture_amount = {
        'amount': {
            'currency_code': 'USD',
            'value': order_amount,
        }
    }

    # Capture the payment
    capture_response = requests.post(
        f'https://api.sandbox.paypal.com/v2/payments/authorizations/{authorization_id}/capture',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        },
        json=capture_amount
    )

    capture = capture_response.json()

    # Check if the payment was successful
    if capture_response.status_code == 201:
        print('Payment captured successfully')
        capture = capture_response.json()
        print(capture)
    else:
        print('An error occurred while capturing the payment')
        error = capture_response.json()
        print(error)

    return JsonResponse(capture)


@login_required
def place_order(request):
    total_amount = request.POST.get('total_amount')

    # Get the address entry
    address_id = request.session['selected_address_id']
    address = Address.objects.get(pk=address_id)

    # Create an order entry
    order_id = request.POST.get('order_id')

    with transaction.atomic():
        order = Order.objects.create(
            id=order_id,
            user=request.user,
            recipient_name=address.recipient_name,
            street_address=address.street_address,
            apartment_address=address.apartment_address,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
            phone_number=address.phone_number,
            total_amount=total_amount,
        )

        # Get the cart item ids of the ordered items from the session
        cart_item_ids = request.session['cart_item_ids']

        # Retrieve cart item info and create order items
        for cart_item_id in cart_item_ids:
            cart_item = CartItem.objects.get(pk=cart_item_id)
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                unit_price=cart_item.product.price,
                quantity=cart_item.quantity
            )
            cart_item.delete()

    # Delete cart item ids session data
    del request.session['cart_item_ids']

    # Redirect to the orders page
    return redirect(reverse('transactions:orders'))


@login_required
def orders(request):
    # Get the orders
    orders = Order.objects.filter(user=request.user).prefetch_related('order_items')
    context = {
        'orders': orders
    }
    return render(request, 'transactions/orders.html', context)
