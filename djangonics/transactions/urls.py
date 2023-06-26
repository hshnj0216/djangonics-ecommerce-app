from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('authorize_payment/', views.authorize_payment, name='authorize_payment'),
    path('capture_payment/', views.capture_payment, name='capture_payment'),
    path('place_order/', views.place_order, name='place_order'),
    path('orders/', views.orders, name='orders'),
]