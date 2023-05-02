from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Cart, CartItem
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchVector


# Create your views here.
def home(request):
    return render(request, 'products/home.html')


def browse_all(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/browse_all.html', {'products': products, 'categories': categories})


def product_details(request, slug, id):
    product = get_object_or_404(Product, pk=id)
    stock_range = range(1, product.stock + 1)
    print(stock_range)
    return render(request, 'products/product_details.html', {'product': product, 'range': stock_range})


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render()


def filter_products(request):
    # get the selected categories from the request parameters
    categories = request.GET.get('categories', '').split(',')

    # filter the products based on the selected categories
    if len(categories) == 1 and categories[0] == '':
        queryset = Product.objects.all()
    else:
        queryset = Product.objects.filter(category__slug__in=categories)
        print(f"filter by categories initiated, queryset is {queryset}")

    # apply price filters if provided
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if max_price and min_price and not (min_price == 'NaN' or max_price == 'NaN'):
        queryset = queryset.filter(price__range=(min_price, max_price))

    return render(request, 'products/product_list_partial.html', {'products': queryset})

def search_products(request):
    query = request.GET.get('query')
    products = Product.objects.annotate(search=SearchVector('name', 'category__name'),).filter(search=SearchQuery(query ))
    categories = Category.objects.all()
    return render(request, 'products/search.html', {'products': products, 'query': query, 'categories': categories})

def cart(request):
    return render(request, 'products/cart.html')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    cart = user.cart

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
    if not created:
        cart_item.quantity += 1
        cart_item.save()

#@login_required
#def buy_now(request):


