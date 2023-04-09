from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
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
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='product_seller', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    units_sold = models.IntegerField(default=0)
    description = models.TextField()
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'products'
        ordering = ('-created_at',)


    def __str__(self):
        return self.name