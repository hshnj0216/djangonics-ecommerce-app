import json
import uuid
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages
from .models import User
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
            print(f"user is {user} ")
        if user is not None:
            response = get_cart_item_count(request=request, user=user)
            cart_item_count = json.loads(response.content)['cart_item_count']
            request.session['cart_item_count'] = cart_item_count
            auth_login(request, user=user)
            print(f"session item count: {request.session['cart_item_count']}")
            return redirect('products:home')
        else:
            error_message = "Invalid email or password."
            context['error_message'] = error_message
            return render(request, "accounts/login.html", context)

def logout(request):
    auth_logout(request)
    return redirect(reverse("products:home"))

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        cart = Cart.objects.create(user=instance)
        cart.save()

