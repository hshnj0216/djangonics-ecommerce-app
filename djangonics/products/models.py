import io
from io import BytesIO
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils import timezone
from decimal import Decimal
from storages.backends.s3boto3 import S3Boto3Storage
from PIL import Image
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

    def get_discounted_price(self):
        if hasattr(self, 'discount'):
            discount = self.discount
            now = timezone.now()
            if discount.start_date <= now <= discount.end_date:
                discount_value = Decimal(discount.value) / 100
                return (self.price - (self.price * discount_value)).quantize(Decimal('0.01'))
            return self.price

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
        price = self.product.get_discounted_price() if hasattr(self.product, 'discount') else self.product.price
        self.total_price = self.quantity * price
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product-images')
    is_main = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.image:
            # Open the image using Pillow
            image = Image.open(self.image)

            # Assign file names and paths
            orig_file_name = self.image.name
            low_quality_file_name = f'low-{self.image.name}'
            file_path = f'{self.product.id}/high-{orig_file_name}'
            low_quality_file_path = f'{self.product.id}/{low_quality_file_name}'

            # Calculate the new dimensions while maintaining the aspect ratio
            width, height = image.size
            aspect_ratio = width / height
            new_width = 48
            new_height = int(new_width / aspect_ratio)
            format = image.format
            # Resize the image
            resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

            #Compress the original image
            compressed_image = BytesIO()
            resized_image.save(compressed_image, format=format, optimize=True, quality=70)
            compressed_image.seek(0)

            # Save the resized image to a buffer
            buffer = io.BytesIO()
            resized_image.save(buffer, format=format)
            buffer.seek(0)

            # Create the InMemoryUploadedFile with the resized image
            low_quality_image = InMemoryUploadedFile(
                buffer,
                None,
                low_quality_file_name,
                f'image/{format.lower()}',
                buffer.tell,
                None
            )

            # Use the S3Boto3Storage backend to upload the original and low-quality images to IBM COS
            storage = S3Boto3Storage(bucket_name=settings.AWS_STORAGE_BUCKET_NAME, endpoint_url=settings.AWS_S3_ENDPOINT_URL)
            storage.save(file_path, self.image)
            storage.save(low_quality_file_path, low_quality_image)

            # Update the image field to use the IBM COS URL
            self.image = f'{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{file_path}'

        super().save(*args, **kwargs)

class Discount(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='discount')
    value = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.OneToOneField(Rating, on_delete=models.CASCADE, related_name='review')
    title = models.CharField(max_length=120)
    content = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('rating', 'user', 'product')


