from django.contrib import admin
from django import forms
from .models import Category, Product, ProductImage


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

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    inlines = [ProductImageInline]
    list_display = ['name', 'slug', 'price', 'stock', 'created_at', 'updated_at']
    list_editable = ['price', 'stock', ]
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image',)
    list_editable = ['image']
