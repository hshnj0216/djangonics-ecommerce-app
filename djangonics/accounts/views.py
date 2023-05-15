import json
import uuid
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from .models import User, Address
from products.views import get_cart_item_count
from products.models import Cart
from django.dispatch import receiver
from django.db.models.signals import post_save
import logging
logger = logging.getLogger(__name__)

# Create your views here.
def signup(request):
    #if the request is GET render the template
    if request.method == "GET":
        return render(request, 'accounts/signup.html')
    #if the request if POST process the registration
    if request.method == "POST":
        context = {}
        #extract credentials
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        contact_number =request.POST['contact_number']
        password = request.POST['password']
        #generate username
        username = email.split('@')[0]+str(uuid.uuid4()).replace('-', '')[:10]
        #create user
        User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            contact_number=contact_number,
            password=password,
            username=username
        )
        success_message = "Account created successfully, you can now log in."
        context['success_message'] = success_message
        return render(request,  'accounts/login.html', context)

def login(request):
    context = {}
    if request.method == "GET":
        return render(request, 'accounts/login.html')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if email and password:
            user = authenticate(email=email, password=password)
        if user is not None:
            response = get_cart_item_count(request=request, user=user)
            cart_item_count = json.loads(response.content)['cart_item_count']
            request.session['cart_item_count'] = cart_item_count
            auth_login(request, user=user)
            return redirect('products:home')
        else:
            error_message = "Invalid email or password."
            context['error_message'] = error_message
            return render(request, "accounts/login.html", context)

def logout(request):
    auth_logout(request)
    return redirect(reverse("products:home"))

def account(request):
    return render(request, 'accounts/account.html')

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        cart = Cart.objects.create(user=instance)
        cart.save()

@login_required
def addresses(request):
    addresses = Address.objects.all().order_by('-is_default')
    return render(request, 'accounts/addresses.html', {'addresses': addresses})

@login_required
def add_address(request):
    # retrieve form data from AJAX request
    full_name = request.POST.get('full_name')
    address_line_1 = request.POST.get('address_line_1')
    address_line_2 = request.POST.get('address_line_2')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip_code = request.POST.get('zip')
    phone_number = request.POST.get('phone_number')

    # perform some logic to add the address to the database
    address, created = Address.objects.update_or_create(
        user=request.user,
        recipient_name=full_name,
        street_address=address_line_1,
        apartment_address=address_line_2,
        city=city,
        state=state,
        zip_code=zip_code,
        phone_number=phone_number,
    )

    # return a JSON response indicating success or failure and the ID of the newly created address
    if created:
        return JsonResponse({'success': True, 'id': address.id}, status=200)
    else:
        return JsonResponse({'success': False, 'error': 'Address already exists'}, status=400)

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)

    #if GET request, send the data
    if request.method == 'GET':
        data = {'address': address}
        return JsonResponse()


@login_required
def set_default_address(request, address_id):
    # get all addresses for the user
    addresses = Address.objects.filter(user=request.user)

    # set is_default to False for all addresses except the current one
    addresses.exclude(pk=address_id).update(is_default=False)

    # set the current address to default
    current_address = Address.objects.get(pk=address_id)
    current_address.is_default = True
    current_address.save()

    sorted_addresses = Address.objects.filter(user=request.user).order_by('-is_default')

    return render(request, 'accounts/address_list_partial.html', {'addresses': sorted_addresses})

def remove_address(request, address_id):
    #get the address to remove
    address =  Address.objects.get(pk=address_id)
    address.delete()
    sorted_addresses = Address.objects.filter(user=request.user).order_by('-is_default')
    return render(request, 'accounts/address_list_partial.html', {'addresses': sorted_addresses})

def checkout(request):
    context = {}
    #get the user's addresses
    addresses = Address.objects.filter(user=request.user)
    context['addresses'] = addresses
    #get the user's cards
    return render(request, 'accounts/checkout.html', context)

