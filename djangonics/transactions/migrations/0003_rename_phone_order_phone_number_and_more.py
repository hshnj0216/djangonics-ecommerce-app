# Generated by Django 4.2 on 2023-06-24 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_rename_address_line1_order_apartment_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='phone',
            new_name='phone_number',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='zipcode',
            new_name='zip_code',
        ),
    ]