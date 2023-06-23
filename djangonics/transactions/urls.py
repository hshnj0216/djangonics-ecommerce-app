from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('authorize_payment/', views.authorize_payment, name='authorize_payment'),
    path('capture_payment/', views.capture_payment, name='capture_payment'),
    path('orders/', views.orders, name='orders'),
]