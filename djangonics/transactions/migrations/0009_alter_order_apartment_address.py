# Generated by Django 4.2 on 2024-02-10 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0008_alter_order_apartment_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='apartment_address',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
