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
        print(f"minmax block run, min_price is {min_price} and max_price is {max_price}")
        print(f"filter by price initiated, current queryset has items {len(queryset)}")
        queryset = queryset.filter(price__range=(min_price, max_price))
        print(f"after queryset length is {len(queryset)}")

    return render(request, 'products/product_list_partial.html', {'products': queryset})

def search_products(request):
    query = request.GET.get('query_string')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'products/product_list_partial.html', {'products': products})