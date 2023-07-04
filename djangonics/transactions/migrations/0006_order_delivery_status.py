# Generated by Django 4.2 on 2023-06-28 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_alter_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_status',
            field=models.CharField(choices=[('Processing', 'Processing'), ('Not Shipped', 'Not Shipped'), ('Shipped', 'Shipped'), ('In Transit', 'In Transit'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered')], default='Processing', max_length=20),
        ),
    ]