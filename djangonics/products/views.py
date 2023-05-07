from botocore.config import Config
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from .models import Product, Category, Cart, CartItem, Rating
from django.db.models import Sum, Avg, Prefetch
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchVector
import boto3
from django.conf import settings


# Create your views here.
def home(request):
    return render(request, 'products/home.html')


def browse_all(request):
    products = Product.objects.prefetch_related(
        Prefetch('ratings', queryset=Rating.objects.all(), to_attr='product_ratings')
    ).annotate(average_rating=Avg('ratings__value')).order_by('-created_at')
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
    cart_item.quantity = quantity
    cart_item.save()
    # get the number of items from the cart for the indicator
    cart_item_count = cart.items.aggregate(Sum('quantity'))['quantity__sum']
    request.session['cart_item_count'] = cart_item_count
    data = {'cart_item_count': cart_item_count}
    return JsonResponse(data)

def get_images(request, product_id):
    # First, check if the response is already cached
    cache_key = f'product_images_{product_id}'
    cached_data = cache.get(cache_key)
    if cached_data:
        return JsonResponse(cached_data)

    # Set up the IBM COS client
    cos_client = boto3.client('s3',
                                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                config=Config(signature_version='s3v4'),
                                region_name='jp-tok'
                             )

    # Get the list of objects in the bucket
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    prefix = f"{product_id}/"
    response = cos_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    # Generate a list of URLs for the image objects
    if 'Contents' in response:
        data = {'img_urls': [f"{settings.AWS_S3_ENDPOINT_URL}/{bucket_name}/{obj['Key']}" for obj in response['Contents']]}
    else:
        data = []

    # Cache the response
    cache.set(cache_key, data)

    return JsonResponse(data)

