# Generated by Django 4.2 on 2023-05-05 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_cartitem_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
