from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('browse_all/', views.browse_all, name='browse_all'),
    path('product/<slug:slug>/<int:id>/', views.product_details, name='product_details'),
    path('filter_products/', views.filter_products, name='filter_products'),
    path('search_products/', views.search_products, name='search_products'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('buy_now/<int:product_id>', views.buy_now, name='buy_now'),
    path('cart/', views.cart, name='cart'),
]