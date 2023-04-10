from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    return render(request, 'products/home.html')

def browse_all(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/browse_all.html', {'products': products, 'categories': categories})

def product_details(request, slug, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'products/product_details.html', {'product': product})

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render()