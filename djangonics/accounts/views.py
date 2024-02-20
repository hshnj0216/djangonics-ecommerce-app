import json
import uuid
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.template.loader import render_to_string
from decimal import Decimal

from django.views.decorators.csrf import csrf_exempt

from .models import User, Address
from products.views import get_cart_item_count
from products.models import Cart, CartItem, Product
from transactions.models import Order, OrderItem
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.forms import LoginForm, SignUpForm
from django.contrib import messages


# Create your views here.
def signup(request):
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == "GET":
        form = SignUpForm()
        return render(request, 'accounts/account/signup.html', {'form': form})

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            contact_number = form.cleaned_data.get('contact_number')
            password = form.cleaned_data.get('password')

            User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name, contact_number=contact_number)
            messages.success(request, "Account created successfully, you can now log in.")
            login_form = LoginForm()
            return render(request, 'accounts/account/login.html', {'login_form': login_form})

        else:
            messages.error(request, "There was a problem with your signup data, please try again.")
            return render(request, 'accounts/account/signup.html', {'form': form})


def login(request):
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, 'accounts/account/login.html', {'login_form': login_form})
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                response = get_cart_item_count(request=request, user=user)
                cart_item_count = json.loads(response.content)['cart_item_count']
                request.session['cart_item_count'] = cart_item_count
                auth_login(request, user=user)
                return redirect('products:home')
        messages.error(request, 'Invalid credentials.')
    else:
        form = LoginForm()
    return render(request, 'accounts/account/login.html', {'login_form': form})



def logout(request):
    auth_logout(request)
    return redirect(reverse("products:home"))


def account(request):
    addresses = Address.objects.filter(user=request.user).order_by('-is_default')
    orders = Order.objects.prefetch_related(
        Prefetch('order_items', queryset=OrderItem.objects.all(), to_attr='items')
    ).filter(user=request.user)
    response = get_cart_item_count(request=request, user=request.user)
    cart_item_count = json.loads(response.content)['cart_item_count']
    request.session['cart_item_count'] = cart_item_count
    context = {
        'addresses': addresses,
        'orders': orders,
    }
    return render(request, 'accounts/account/account.html', context)


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        cart = Cart.objects.create(user=instance)
        cart.save()


@login_required
def add_address(request):
    # retrieve form data from AJAX request
    recipient_name = request.POST.get('recipient_name')
    street_address = request.POST.get('street_address')
    apartment_address = request.POST.get('apartment_address')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip_code = request.POST.get('zip_code')
    phone_number = request.POST.get('phone_number')

    # perform some logic to add the address to the database
    address, created = Address.objects.update_or_create(
        user=request.user,
        recipient_name=recipient_name,
        street_address=street_address,
        apartment_address=apartment_address,
        city=city,
        state=state,
        zip_code=zip_code,
        phone_number=phone_number,
    )

    # return a JSON response indicating success or failure and the ID of the newly created address
    if created:
        address = Address.objects.filter(user=request.user).latest('id')
        print(address)
        return render(request, 'accounts/account/address_card_partial.html', {'address': address})
    else:
        return JsonResponse({'success': False, 'error': 'Address already exists'}, status=400)


@login_required
@csrf_exempt
def edit_address(request, address_id):
    if request.method == 'GET':
        address = Address.objects.get(pk=address_id)
        return render(request, 'accounts/edit_address_form_partial.html', {'address': address})


def save_address_changes(request):
    if request.method == 'POST':
        address_id = request.POST.get('id')
        address = Address.objects.get(pk=address_id)
        form_data = request.POST.dict()
        address.__dict__.update(**form_data)
        address.save()
    return render(request, 'accounts/account/address_card_partial.html', {'address': address})



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

    return render(request, 'accounts/account/address_list_partial.html', {'addresses': sorted_addresses})


@login_required
def remove_address(request, address_id):
    # get the address to remove
    address = Address.objects.get(pk=address_id)
    address.delete()
    sorted_addresses = Address.objects.filter(user=request.user).order_by('-is_default')
    return render(request, 'accounts/account/address_list_partial.html', {'addresses': sorted_addresses})


@login_required
def checkout(request):
    if request.POST.get('buy_now'):
        product_id = int(request.POST.get('product_id'))
        qty = int(request.POST.get('qty'))
        product = Product.objects.get(pk=product_id)
        selected_items = [{
            'product': product,
            'quantity': qty,
        }]
        request.session['is_buy_now'] = True
    else:
        selected_item_ids = request.POST.getlist('cart_item')
        selected_items = CartItem.objects.filter(id__in=selected_item_ids)
        selected_items = [{'cart_item_id': item.id, 'product': item.product, 'quantity': item.quantity} for item in
                          selected_items]
        request.session['is_buy_now'] = False

    # Store the selected items in the session
    checkout_item_ids = []
    for item in selected_items:
        checkout_item = {'product_id': item['product'].id, 'quantity': item['quantity']}
        if not request.session['is_buy_now']:
            checkout_item['cart_item_id'] = item['cart_item_id']
        checkout_item_ids.append(checkout_item)
    request.session['checkout_item_ids'] = checkout_item_ids

    # Calculate total price and total item count
    total_price = 0
    total_item_count = 0
    for item in selected_items:
        total_price += item['product'].price * item['quantity']
        total_item_count += item['quantity']

    tax_rate = Decimal(0.1)
    tax = Decimal(total_price) * tax_rate
    shipping_and_handling_rate = Decimal(100)
    # get the user's addresses
    addresses = Address.objects.filter(user=request.user)

    context = {
        'addresses': addresses,
        'selected_items': selected_items,
        'total_price': total_price,
        'total_item_count': total_item_count,
        'tax': tax,
        'order_total': total_price + tax + shipping_and_handling_rate
    }

    return render(request, 'accounts/checkout/checkout.html', context)


def use_address(request):
    address_id = request.POST['address_id']
    address = Address.objects.get(pk=address_id)
    request.session['selected_address_id'] = address_id
    address_context = {
        'address': address,
    }
    selected_address_html = render_to_string('accounts/checkout/selected_address.html', address_context, request)
    data = {
        'selected_address_html': selected_address_html,
    }
    return JsonResponse(data)


def change_selected_address(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'accounts/checkout/address_selection_partial.html', {'addresses': addresses})

def add_address_from_checkout(request):
    # retrieve form data from AJAX request
    recipient_name = request.POST.get('recipient_name')
    street_address = request.POST.get('street_address')
    apartment_address = request.POST.get('apartment_address')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip_code = request.POST.get('zip_code')
    phone_number = request.POST.get('phone_number')

    # perform some logic to add the address to the database
    address, created = Address.objects.update_or_create(
        user=request.user,
        recipient_name=recipient_name,
        street_address=street_address,
        apartment_address=apartment_address,
        city=city,
        state=state,
        zip_code=zip_code,
        phone_number=phone_number,
    )

    # return a JSON response indicating success or failure and the ID of the newly created address
    if created:
        address = Address.objects.filter(user=request.user).latest('id')
        return render(request, 'accounts/checkout/address_selection_entry.html', {'address': address})
    else:
        return JsonResponse({'success': False, 'error': 'Address already exists'}, status=400)

def save_address_changes_from_checkout(request):
    if request.method == 'POST':
        address_id = request.POST.get('id')
        address = Address.objects.get(pk=address_id)
        form_data = request.POST.dict()
        address.__dict__.update(**form_data)
        address.save()
    return render(request, 'accounts/checkout/address_selection_entry.html', {'address': address})


def select_payment_method(request):
    return render(request, 'accounts/checkout/selected_payment.html')
