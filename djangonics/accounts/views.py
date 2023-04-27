from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
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
        #extract credentials
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']


def login(request):
    if request.method == "GET":
        return render(request, 'accounts/login.html')
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if username:
            user = authenticate(username, password)
        if email:
            user = authenticate(email, password)