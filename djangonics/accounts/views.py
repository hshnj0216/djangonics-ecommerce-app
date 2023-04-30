import uuid
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import User
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



def login_user(request):
    context = {}
    if request.method == "GET":
        return render(request, 'accounts/login.html')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if email and password:
            user = authenticate(email=email, password=password)
            print(user)
        if user is not None:
            login(request, user=user)
            return redirect(reverse("products:home"))
        else:
            error_message = "Invalid email or password."
            context['error_message'] = error_message
            return render(request, "accounts/login.html", context)
