from django.contrib import admin
from django import forms
from .models import Category, Product, ProductImage, Discount


# Register your models here
class ProductForm(forms.ModelForm):
    is_main = forms.BooleanField(required=False)
    class Meta:
        model = Product
        fields = '__all__'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage

class DiscountInline(admin.TabularInline):
    model = Discount

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    inlines = [ProductImageInline, DiscountInline]
    list_display = ['name', 'slug', 'price', 'stock', 'units_sold', 'created_at', 'updated_at']
    list_editable = ['price', 'stock',]
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image',)
    list_editable = ['image']

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('value', )
