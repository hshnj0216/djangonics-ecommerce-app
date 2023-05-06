import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.urls import reverse
from storages.backends.s3boto3 import S3Boto3Storage

from accounts.models import User


# Create your models here.
class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    COMPUTERS_LAPTOPS = 'computers_laptops'
    SMARTPHONES_TABLETS = 'smartphones_tablets'
    GAMING_CONSOLES_ACCESSORIES = 'gaming_consoles_accessories'
    AUDIO_VIDEO_EQUIPMENT = 'audio_video_equipment'
    STORAGE_DEVICES = 'storage_devices'

    CATEGORY_CHOICES = [
        (COMPUTERS_LAPTOPS, 'Computers & Laptops'),
        (SMARTPHONES_TABLETS, 'Smartphones & Tablets'),
        (GAMING_CONSOLES_ACCESSORIES, 'Gaming Consoles & Accessories'),
        (AUDIO_VIDEO_EQUIPMENT, 'Audio & Video Equipment'),
        (STORAGE_DEVICES, 'Storage Devices'),
    ]
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    units_sold = models.IntegerField(default=0)
    description = models.TextField()
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'products'
        ordering = ('-created_at',)


    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('cart', 'product')

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.product.price
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product-images')
    is_main = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.image:
            # Get the file name and path within the S3 bucket
            file_name = self.image.name
            file_path = f'{self.product.id}/{file_name}'

            # Use the S3Boto3Storage backend to upload the file to IBM COS
            storage = S3Boto3Storage(bucket_name=settings.AWS_STORAGE_BUCKET_NAME, endpoint_url=settings.AWS_S3_ENDPOINT_URL)
            file = self.image.file
            storage.save(file_path, file)

            # Update the image field to use the IBM COS URL
            self.image = f'{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{file_path}'

        super().save(*args, **kwargs)

