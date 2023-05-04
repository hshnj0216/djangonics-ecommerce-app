# Generated by Django 4.2 on 2023-05-03 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_cart_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
