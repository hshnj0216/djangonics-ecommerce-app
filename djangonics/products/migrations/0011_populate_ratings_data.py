# Generated by Django 4.2 on 2023-05-07 16:58
from random import randint
from django.db import migrations

def generate_random_rating():
    return randint(3, 5)

def populate_ratings(apps=None, schema_editor=None):
    Rating = apps.get_model('products', 'Rating')
    Product = apps.get_model('products', 'Product')
    products = Product.objects.all()
    for product in products:
        for i in range(randint(10, 20)):
            rating = generate_random_rating()
            Rating.objects.create(product=product, value=rating)

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_rating'),
    ]

    operations = [
        migrations.RunPython(populate_ratings)
    ]




