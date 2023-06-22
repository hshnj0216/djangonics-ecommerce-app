from django.db import models

from accounts.models import User
from products.models import Product


# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('Archived', 'Archived'),
        ('Canceled', 'Canceled')
    )
    RETURN_STATUS_CHOICES = (
        ('Not Returned', 'Not Returned'),
        ('Return Requested', 'Return Requested'),
        ('Return Approved', 'Return Approved'),
        ('Return Rejected', 'Return Rejected'),
        ('Returned', 'Returned')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    address_line1 = models.CharField(max_length=250)
    address_line2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_key = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    return_status = models.CharField(max_length=20, choices=RETURN_STATUS_CHOICES, default='Not Returned')

    class Meta:
        ordering: ('-created',)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    @property
    def total_price(self):
        return self.unit_price * self.quantity