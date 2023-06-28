from django.db import migrations, models
from django.conf import settings

def create_transactions_order_table(apps, schema_editor):
    Order = apps.get_model('transactions', 'Order')
    db_alias = schema_editor.connection.alias
    fields = [
        ('id', models.CharField(max_length=100, primary_key=True)),
        ('user', models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)),
        ('recipient_name', models.CharField(max_length=100)),
        ('street_address', models.CharField(max_length=250)),
        ('apartment_address', models.CharField(max_length=250)),
        ('city', models.CharField(max_length=25)),
        ('state', models.CharField(max_length=25)),
        ('phone_number', models.CharField(max_length=20)),
        ('zip_code', models.CharField(max_length=20)),
        ('total_amount', models.DecimalField(decimal_places=2, max_digits=8)),
        ('created_at', models.DateTimeField(auto_now_add=True)),
        ('updated_at', models.DateTimeField(auto_now=True)),
        ('status', models.CharField(choices=[('Open', 'Open'), ('Archived', 'Archived'), ('Canceled', 'Canceled')], default='Open', max_length=20)),
        ('delivery_status', models.CharField(choices=[('Processing', 'Processing'), ('Not Shipped', 'Not Shipped'), ('Shipped', 'Shipped'), ('In Transit', 'In Transit'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered')], default='Processing', max_length=20)),
        ('return_status', models.CharField(choices=[('Not Returned', 'Not Returned'), ('Return Requested', 'Return Requested'), ('Return Approved', 'Return Approved'), ('Return Rejected', 'Return Rejected'), ('Returned', 'Returned')], default='Not Returned', max_length=20))
    ]
    table = Order._meta.db_table
    schema_editor.create_model(Order)
    # Create any required indexes or constraints
    for index in Order._meta.indexes:
        schema_editor.add_index(Order, index)

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_transactions_order_table),
    ]
