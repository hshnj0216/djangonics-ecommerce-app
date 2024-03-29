from django.urls import path
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
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('save_address_changes/', views.save_address_changes, name='save_address_changes'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_address_from_checkout/', views.add_address_from_checkout, name='add_address_from_checkout'),
    path('save_address_changes_from_checkout/', views.save_address_changes_from_checkout, name='save_address_changes_from_checkout'),
    path('use_address/', views.use_address, name='use_address'),
    path('change_selected_address/', views.change_selected_address, name='change_selected_address'),
    path('select_payment_method/', views.select_payment_method, name='select_payment_method'),
]