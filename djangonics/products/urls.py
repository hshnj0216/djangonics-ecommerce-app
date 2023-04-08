from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.browse_all, name='browse_all'),
    path('product/<slug:slug>/<int:id>/', views.product_details, name='product_details'),
]