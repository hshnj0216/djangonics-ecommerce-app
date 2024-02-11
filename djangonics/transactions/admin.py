from django.contrib import admin
from .models import Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['status', 'user']
    readonly_fields = ['total_amount', 'id', 'user', 'created_at', 'updated_at']