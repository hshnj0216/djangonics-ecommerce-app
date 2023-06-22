from django.contrib.auth.decorators import login_required
from .models import Order
from django.shortcuts import render
import json
import requests
import sys
from django.http import JsonResponse


# Create your views here.
@login_required
def authorize_payment(request):
    print('authorize_payment')
    client_id = 'ATq1dwh2EUeN17EwoFcOdVylRg8jJAIt_9yDXDt83oO2EE2vwc8uUC-5LPcn6-7gPKsOVR0PjKjZG4x_'
    client_secret = 'ECe8YLL6r3g0D57lwc7-s4CPh2EVgWNlxEdn81K8vizlEENGJh9MF-hK0DfLeUTkILV3FlK-5AElab6V'

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

    print(authorization)

    return JsonResponse(authorization)