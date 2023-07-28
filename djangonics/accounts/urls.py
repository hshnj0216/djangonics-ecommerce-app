from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('account/', views.account, name='account'),
    path('add_address/', views.add_address, name='add_address'),
    path('set_default_address/<int:address_id>/', views.set_default_address, name='set_default_address'),
    path('remove_address/<int:address_id>/', views.remove_address, name='remove_address'),
    path('edit_address/', views.edit_address, name='edit_address'),
    path('checkout/', views.checkout, name='checkout'),
    path('use_address/', views.use_address, name='use_address'),
    path('change_selected_address/', views.change_selected_address, name='change_selected_address'),
    path('select_payment_method/', views.select_payment_method, name='select_payment_method'),
]