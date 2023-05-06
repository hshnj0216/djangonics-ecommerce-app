import botocore
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Cart, CartItem, ProductImage
from django.db.models import Sum
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchVector
import boto3
from django.conf import settings


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
    product_images = product.images.all()
    return render(request, 'products/product_details.html',
                  {'product': product, 'range': stock_range, 'product_images': product_images})


def filter_products(request):
    # get the selected categories from the request parameters
    categories = request.GET.get('categories', '').split(',')

    # filter the products based on the selected categories
    if len(categories) == 1 and categories[0] == '':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category__slug__in=categories)

    # apply price filters if provided
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if max_price and min_price and not (min_price == 'NaN' or max_price == 'NaN'):
        products = products.filter(price__range=(min_price, max_price))

    return render(request, 'products/product_list_partial.html', {'products': products})


def search_products(request):
    query = request.GET.get('query')
    # search the name and category name columns
    products = Product.objects.annotate(search=SearchVector('name', 'category__name'), ).filter(
        search=SearchQuery(query))
    categories = Category.objects.all()
    return render(request, 'products/search.html', {'products': products, 'query': query, 'categories': categories})


@login_required
def cart(request):
    context = {}
    # Get user's cart
    cart = Cart.objects.get(user=request.user)

    # Get cart items
    cart_items = cart.items.all()
    products = []
    for item in cart_items:
        product_quantity_range = range(1, item.product.stock + 1)
        print(product_quantity_range)
        product_info = {
            'id': item.product.id,
            'price': item.product.price,
            'name': item.product.name,
            'quantity': item.quantity,
            'total_price': item.total_price,
            'image': item.product.image,
            'slug': item.product.slug,
            'range': product_quantity_range,
        }
        products.append(product_info)
    context['products'] = products
    return render(request, 'products/cart.html', context)


@login_required
def add_to_cart(request):
    # get the product from the POST data
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)

    # get the quantity from the POST data
    quantity = int(request.POST.get('qty'))

    # get the user's cart
    user = request.user
    cart = user.cart

    # check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # if the item was created, assign values
    if created:
        cart_item.quantity = quantity
        cart_item.total_price = cart_item.quantity * product.price
        cart_item.save()

    # if the item already exists, update values
    else:
        cart_item.quantity += quantity
        cart_item.total_price += cart_item.quantity * product.price
        cart_item.save()

    # get the number of items from the cart for the indicator
    cart_item_count = cart.items.aggregate(Sum('quantity'))['quantity__sum']
    request.session['cart_item_count'] = cart_item_count

    return JsonResponse({'cart_item_count': cart_item_count})


# @login_required
def buy_now(request):
    if request.method == "GET":
        pass
    if request.method == "POST":
        pass


def get_cart_item_count(request, user):
    cart_item_count = request.session.get('cart_item_count')
    if cart_item_count is None:
        cart_item_count = CartItem.objects.filter(cart__user=user).aggregate(Sum('quantity'))['quantity__sum']
        if cart_item_count is None:
            cart_item_count = 0
            request.session['cart_item_count'] = cart_item_count
    print(f"cart item count: {cart_item_count}")
    data = {'cart_item_count': cart_item_count}
    return JsonResponse(data)


@login_required
def remove_item(request, product_id):
    cart_item = get_object_or_404(CartItem, product_id=product_id)
    cart_item.delete()
    return redirect('products:cart')


@login_required
def update_item_quantity(request):
    product_id = request.POST['product_id']
    quantity = int(request.POST['qty'])
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    cart = user.cart
    cart_item = get_object_or_404(CartItem, product=product, cart=cart)
    print(f"Cart Item quantity was: {cart_item.quantity}")
    cart_item.quantity = quantity
    cart_item.save()
    print(f"Cart Item quantity now: {cart_item.quantity}")
    # get the number of items from the cart for the indicator
    cart_item_count = cart.items.aggregate(Sum('quantity'))['quantity__sum']
    request.session['cart_item_count'] = cart_item_count
    data = {'cart_item_count': cart_item_count}
    return JsonResponse(data)

def get_item(bucket_name, item_name):
    print("Retrieving item from bucket: {0}, key: {1}".format(bucket_name, item_name))
    try:
        file = cos.Object(bucket_name, item_name).get()
        print("File Contents: {0}".format(file["Body"].read()))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve file contents: {0}".format(e))
