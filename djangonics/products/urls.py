from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.browse_all, name='browse_all'),
    path('<slug:slug>/', views.product_details, name='product_details'),
]