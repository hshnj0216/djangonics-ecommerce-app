from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# Create your views here.
def home(request):
    return render(request, 'products/home.html')

def browse_all(request):
    products = Product.objects.all()
    return render(request, 'products/browse_all.html', {'products': products})

def product_details(request, slug, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'products/product_details.html', {'product': product})