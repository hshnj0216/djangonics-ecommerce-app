from botocore.config import Config
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from django.template.loader import render_to_string
from django.utils.cache import patch_response_headers
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category, Cart, CartItem, Rating, Discount, Review
from django.db.models import Sum, Avg, Prefetch, Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.core.paginator import Paginator
import boto3
from django.conf import settings
from PIL import Image

from transactions.models import Order


# Create your views here.
def generate_low_quality_image(request, hq_image):
    # open the high quality image
    image = Image.open(hq_image)

    # resize image
    resized_image = image.resize((148, 138))

    # compress image
    compressed_image_path = 'static/images/'
    resized_image.save(compressed_image_path, quality=60)

    # Serve the processed image as a response
    with open(compressed_image_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='image/jpeg')
    return response


def get_products(request):
    products = Product.objects.prefetch_related(
        Prefetch('ratings', queryset=Rating.objects.all(), to_attr='product_ratings'),
        Prefetch('discount', queryset=Discount.objects.all(), to_attr='product_discount')
    ).annotate(
        average_rating=Avg('ratings__value'),
        num_ratings=Count('ratings')
    )

    return products


def get_best_sellers(request):
    products = Product.objects.filter(units_sold__gt=0).order_by('-units_sold'
                                                                 ).prefetch_related(
        Prefetch('ratings', queryset=Rating.objects.all(), to_attr='product_ratings'),
        Prefetch('discount', queryset=Discount.objects.all(), to_attr='product_discount')
    ).annotate(
        average_rating=Avg('ratings__value'),
        num_ratings=Count('ratings')
    )
    return products


def get_todays_deals(request):
    products = Product.objects.filter(discount__gt=0
                                      ).prefetch_related(
        Prefetch('ratings', queryset=Rating.objects.all(), to_attr='product_ratings'),
        Prefetch('discount', queryset=Discount.objects.all(), to_attr='product_discount')
    ).annotate(
        average_rating=Avg('ratings__value'),
        num_ratings=Count('ratings')
    ).order_by('-discount__value')
    return products


def get_new_arrivals(request):
    products = Product.objects.order_by('-created_at'
                                        ).prefetch_related(
        Prefetch('ratings', queryset=Rating.objects.all(), to_attr='product_ratings'),
        Prefetch('discount', queryset=Discount.objects.all(), to_attr='product_discount')
    ).annotate(
        average_rating=Avg('ratings__value'),
        num_ratings=Count('ratings')
    )
    return products


def home(request):
    # Get 5 items from each nav link
    todays_deals = list(enumerate(get_todays_deals(request)[:4], start=1))
    best_sellers = list(enumerate(get_best_sellers(request)[:4], start=1))
    new_arrivals = list(enumerate(get_new_arrivals(request)[:4], start=1))
    context = {
        'todays_deals': todays_deals,
        'best_sellers': best_sellers,
        'new_arrivals': new_arrivals,
    }
    return render(request, 'products/home.html', context)


def browse_all(request):
    products = get_products(request)
    new_arrivals = get_new_arrivals(request)
    best_sellers = get_best_sellers(request)
    discounted_products = get_todays_deals(request)
    categories = Category.objects.all()
    products = list(enumerate(products, start=1))

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'new_arrivals': new_arrivals,
        'best_sellers': best_sellers,
        'discounted_products': discounted_products,
        'categories': categories
    }
    return render(request, 'products/browse_all.html', context)


def todays_deals(request):
    products = get_todays_deals(request)
    categories = Category.objects.all()
    products = list(enumerate(products, start=1))

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request, 'products/todays_deals.html', {'products': products, 'categories': categories})


def best_sellers(request):
    products = get_best_sellers(request)
    categories = Category.objects.all()
    products = list(enumerate(products, start=1))

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request, 'products/best_sellers.html', {'products': products, 'categories': categories})


def new_arrivals(request):
    products = get_new_arrivals(request)
    categories = Category.objects.all()
    products = list(enumerate(products, start=1))

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request, 'products/new_arrivals.html', {'products': products, 'categories': categories})


def get_product_details(request, product_id):
    product = Product.objects.prefetch_related(
        Prefetch('ratings', queryset=Rating.objects.all(), to_attr='product_ratings'),
        Prefetch('discount', queryset=Discount.objects.all(), to_attr='product_discount'),
        Prefetch('reviews', queryset=Review.objects.all(), to_attr='product_reviews')
    ).annotate(
        average_rating=Avg('ratings__value'),
        num_ratings=Count('ratings'),
        rating_1=Count('ratings', filter=Q(ratings__value=1)),
        rating_2=Count('ratings', filter=Q(ratings__value=2)),
        rating_3=Count('ratings', filter=Q(ratings__value=3)),
        rating_4=Count('ratings', filter=Q(ratings__value=4)),
        rating_5=Count('ratings', filter=Q(ratings__value=5)),
    ).get(
        pk=product_id
    )
    return product


def can_submit_rating(request, product, product_id):
    if request.user.is_authenticated:
        has_completed_order = Order.objects.filter(
            user=request.user,
            order_items__product_id=product_id,
            delivery_status='Delivered'
        ).exists()
        has_submitted_rating = Rating.objects.filter(
            user=request.user,
            product=product_id
        ).exists()
        if has_completed_order and not has_submitted_rating:
            can_submit_rating = True
        else:
            can_submit_rating = False
        return can_submit_rating


def can_submit_review(request, product_id):
    if request.user.is_authenticated:
        has_completed_order = Order.objects.filter(
            user=request.user,
            order_items__product_id=product_id,
            delivery_status='Delivered'
        ).exists()
        has_submitted_review = Review.objects.filter(
            user=request.user,
            product_id=product_id,
        ).exists()
        if has_completed_order and not has_submitted_review:
            can_submit_review = True
        else:
            can_submit_review = False
        return can_submit_review


def product_details(request, slug, product_id):
    product = get_product_details(request, product_id)
    if product.stock <= 30:
        stock_range = range(1, product.stock + 1)
    else:
        stock_range = range(1, 31)
    # Calculate percentages
    if product.num_ratings > 0:
        rating_1_percentage = (product.rating_1 / product.num_ratings) * 100
        rating_2_percentage = (product.rating_2 / product.num_ratings) * 100
        rating_3_percentage = (product.rating_3 / product.num_ratings) * 100
        rating_4_percentage = (product.rating_4 / product.num_ratings) * 100
        rating_5_percentage = (product.rating_5 / product.num_ratings) * 100
    else:
        rating_1_percentage = 0
        rating_2_percentage = 0
        rating_3_percentage = 0
        rating_4_percentage = 0
        rating_5_percentage = 0

    # get user rating
    user_rating = Rating.objects.filter(user=request.user, product=product).first()
    # Check if the user is allowed to submit a rating
    user_can_submit_rating = can_submit_rating(request, product, product_id)
    # Check if the user is allowed to submit a review
    user_can_submit_review = can_submit_review(request, product_id)

    context = {
        'product': product,
        'user_can_submit_review': user_can_submit_review,
        'user_can_submit_rating': user_can_submit_rating,
        'range': stock_range,
        'user_rating': user_rating.value if user_rating else None,
        'rating_1_percentage': rating_1_percentage,
        'rating_2_percentage': rating_2_percentage,
        'rating_3_percentage': rating_3_percentage,
        'rating_4_percentage': rating_4_percentage,
        'rating_5_percentage': rating_5_percentage,
    }
    return render(request, 'products/product_details.html', context)


@csrf_exempt
def filter_products(request):
    # get the initial products queryset based on the current page
    current_page = request.GET.get('current_page')
    if current_page == 'new_arrivals':
        products = get_new_arrivals(request)
    elif current_page == 'todays_deals':
        products = get_todays_deals(request)
    elif current_page == 'best_sellers':
        products = get_best_sellers(request)
    elif current_page == 'search_products':
        query = request.GET.get('query')
        print(query)
        products = Product.objects.prefetch_related(
            Prefetch('ratings', queryset=Rating.objects.all(), to_attr='product_ratings'),
            Prefetch('discount', queryset=Discount.objects.all(), to_attr='product_discount')
        ).annotate(
            search=SearchVector('name', 'category__name'),
            average_rating=Avg('ratings__value'),
            num_ratings=Count('ratings')
        ).filter(search=SearchQuery(query))
        print(products)
    else:
        products = get_products(request)

    # apply category filters if provided
    categories = request.GET.get('categories', '').split(',')
    if len(categories) == 1 and categories[0] != '':
        products = products.filter(category__slug__in=categories)

    # apply price filters if provided
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if max_price and min_price and not (min_price == 'NaN' or max_price == 'NaN'):
        products = products.filter(price__range=(min_price, max_price))

    # apply rating filter if provided
    rating = request.GET.get('rating')
    print(rating)
    if rating:
        min_rating = float(rating)
        max_rating = min_rating + 1
        products = products.filter(average_rating__gte=min_rating, average_rating__lt=max_rating)

    new_arrivals = products.order_by('-created_at')[:10]
    best_sellers = products.filter(units_sold__gt=0).order_by('-units_sold')
    discounted_products = products.filter(discount__gt=0)

    categories = Category.objects.all()
    products = list(enumerate(products, start=1))
    context = {
        'current_page': current_page,
        'products': products,
        'new_arrivals': new_arrivals,
        'best_sellers': best_sellers,
        'discounted_products': discounted_products,
        'categories': categories
    }
    return render(request, 'products/product_list_partial.html', context)


def search_products(request):
    current_page = request.GET.get('current_page')
    query = request.GET.get('query')

    # search the name and category name columns
    products = Product.objects.prefetch_related(
        Prefetch('ratings', queryset=Rating.objects.all(), to_attr='product_ratings'),
        Prefetch('discount', queryset=Discount.objects.all(), to_attr='product_discount')
    ).annotate(
        search=SearchVector('name', 'category__name'),
        average_rating=Avg('ratings__value'),
        num_ratings=Count('ratings')
    ).filter(search=SearchQuery(query))

    new_arrivals = products.order_by('-created_at')[:10]
    best_sellers = products.filter(units_sold__gt=0).order_by('-units_sold')
    discounted_products = products.filter(discount__gt=0)

    categories = Category.objects.all()
    products = list(enumerate(products, start=1))
    context = {
        'query': query,
        'current_page': current_page,
        'products': products,
        'new_arrivals': new_arrivals,
        'best_sellers': best_sellers,
        'discounted_products': discounted_products,
        'categories': categories
    }
    return render(request, 'products/search.html', context)


@login_required
def cart(request):
    context = {}
    # Get user's cart
    cart = Cart.objects.get(user=request.user)

    # Get cart items
    cart_items = cart.items.all()
    products = []
    qty_range = range(1, 10)
    for item in cart_items:
        product_info = {
            'cart_item_id': item.id,
            'product_id': item.product.id,
            'price': item.product.price,
            'name': item.product.name,
            'quantity': item.quantity,
            'total_price': item.total_price,
            'slug': item.product.slug,
            'discounted_price': item.product.get_discounted_price()
        }
        products.append(product_info)
    context['products'] = products
    context['range'] = qty_range
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


def get_cart_item_count(request, user):
    cart_item_count = request.session.get('cart_item_count')
    if cart_item_count is None:
        cart_item_count = CartItem.objects.filter(cart__user=user).aggregate(Sum('quantity'))['quantity__sum']
        if cart_item_count is None:
            cart_item_count = 0
            request.session['cart_item_count'] = cart_item_count
    data = {'cart_item_count': cart_item_count}
    return JsonResponse(data)


@login_required
@csrf_exempt
def remove_item(request):
    product_id = request.POST['product_id']
    cart_item_id = request.POST['cart_item_id']
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    product = Product.objects.get(id=product_id)
    cart = request.user.cart
    cart_item_count = cart.items.aggregate(quantity_sum=Coalesce(Sum('quantity'), 0))['quantity_sum']
    request.session['cart_item_count'] = cart_item_count
    removed_html = render_to_string('products/removed.html', {'product': product}, request)
    data = {
        'cart_item_count': cart_item_count,
        'removed_html': removed_html,
    }
    return JsonResponse(data)


@login_required
@csrf_exempt
def update_item_quantity(request):
    product_id = request.POST['product_id']
    quantity = int(request.POST['qty'])
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    cart = user.cart
    cart_item = get_object_or_404(CartItem, product=product, cart=cart.id)
    if quantity != 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    # get the number of items from the cart for the indicator
    cart_item_info = {
        'cart_item_id': cart_item.id,
        'product_id': cart_item.product.id,
        'price': cart_item.product.price,
        'name': cart_item.product.name,
        'quantity': cart_item.quantity,
        'total_price': cart_item.total_price,
        'slug': cart_item.product.slug,
    }
    cart_item_count = cart.items.aggregate(Sum('quantity'))['quantity__sum']
    request.session['cart_item_count'] = cart_item_count
    qty_range = range(1, 10)
    cart_item_options_html = render_to_string('products/cart_item_options_partial.html',
                                              {'product': cart_item_info, 'range': qty_range}, request)
    data = {
        'cart_item_count': cart_item_count,
        'cart_item_options_html': cart_item_options_html,
    }
    return JsonResponse(data)


@csrf_exempt
def get_images(request):
    # First, check if the response is already cached
    product_id = request.POST.get('product_id')
    quality = request.POST.get('quality')
    cache_key = f'product_images_{quality}_{product_id}'
    cached_data = cache.get(cache_key)
    if cached_data:
        return JsonResponse(cached_data)

    try:
        # Set up the IBM COS client
        session = boto3.session.Session()
        cos_client = session.client('s3',
                                    endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                    config=Config(signature_version='s3v4'),
                                    region_name='jp-tok'
                                    )

        # Get the list of objects in the bucket
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        prefix = f"{product_id}/{quality}-"
        response = cos_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        # Generate a list of URLs for the image objects
        if 'Contents' in response:
            data = {
                'img_urls': [f"{settings.AWS_S3_ENDPOINT_URL}/{bucket_name}/{obj['Key']}" for obj in response['Contents']],
                'status': 'success',
            }
        else:
            data = {
                'status': 'failed',
            }

    except (BotoCoreError, ClientError):
        # If accessing the bucket fails, serve the static files
        static_url = settings.STATIC_URL
        data = {
            'img_urls': [f"{static_url}{product_id}/{quality}-{i}.jpg" for i in range(1, 6)],  # adjust as needed
            'status': 'success',
        }

    # Cache the response
    cache.set(cache_key, data)

    response = JsonResponse(data)

    # Set cache headers
    cache_timeout = 60 * 30
    patch_response_headers(response, cache_timeout=cache_timeout)

    return response


@login_required
@csrf_exempt
def submit_rating(request):
    rating = request.POST.get('rating')
    product_id = request.POST.get('product_id')
    # Get the product object
    product = Product.objects.get(pk=product_id)

    # Create and save a new Rating object
    rating = Rating.objects.create(
        user=request.user,
        product=product,
        value=rating
    )
    rating.save()

    product = get_product_details(request, product_id)

    if product.stock <= 30:
        stock_range = range(1, product.stock + 1)
    else:
        stock_range = range(1, 31)
    # Calculate percentages
    if product.num_ratings > 0:
        rating_1_percentage = (product.rating_1 / product.num_ratings) * 100
        rating_2_percentage = (product.rating_2 / product.num_ratings) * 100
        rating_3_percentage = (product.rating_3 / product.num_ratings) * 100
        rating_4_percentage = (product.rating_4 / product.num_ratings) * 100
        rating_5_percentage = (product.rating_5 / product.num_ratings) * 100
    else:
        rating_1_percentage = 0
        rating_2_percentage = 0
        rating_3_percentage = 0
        rating_4_percentage = 0
        rating_5_percentage = 0

    user_can_submit_rating = False

    # get user rating
    user_rating = Rating.objects.filter(user=request.user, product=product).first()
    print(user_rating)

    context = {
        'product': product,
        'user_can_submit_rating': user_can_submit_rating,
        'range': stock_range,
        'user_rating': user_rating.value,
        'rating_1_percentage': rating_1_percentage,
        'rating_2_percentage': rating_2_percentage,
        'rating_3_percentage': rating_3_percentage,
        'rating_4_percentage': rating_4_percentage,
        'rating_5_percentage': rating_5_percentage,
    }
    return render(request, 'products/customer_rating_partial.html', context)


@login_required
def post_review(request):
    review_title = request.POST.get('review_title')
    review_content = request.POST.get('review_content')
    product_id = request.POST.get('product_id')
    print(f"product_id: {product_id}")
    rating = Rating.objects.filter(user=request.user, product=product_id).first()
    product = Product.objects.get(pk=product_id)
    # Create review
    review = Review.objects.create(
        user=request.user,
        product=product,
        title=review_title,
        content=review_content,
        rating=rating
    )
    review.save()
    can_user_submit_review = False
    product = get_product_details(request, product_id)
    context = {
        'product': product,
        'can_user_submit_review': can_user_submit_review,
        'rating': review.rating
    }
    return render(request, 'products/customer_reviews_partial.html', context)
