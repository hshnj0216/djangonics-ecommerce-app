from django.shortcuts import render
from .models import Product, Category

# Create your views here.
def browse_all(request):
    products = Product.objects.all()
    return render(request, 'products/browse_all.html', {'products': products})