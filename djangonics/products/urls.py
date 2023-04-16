from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('browse_all/', views.browse_all, name='browse_all'),
    path('product/<slug:slug>/<int:id>/', views.product_details, name='product_details'),
    path('filter_products/', views.filter_products, name='filter_products'),
    path('search_products/', views.search_products, name='search_products'),
]