from django.contrib import admin
from django import forms
from .models import Category, Product, ProductImage, Discount, Rating, Review


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

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('value', )
class DiscountInline(admin.TabularInline):
    model = Discount

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0  # this will prevent extra empty forms

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0  # this will prevent extra empty forms


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    inlines = [ProductImageInline, DiscountInline, RatingInline, ReviewInline]
    list_display = ['name', 'slug', 'price', 'stock', 'discount', 'units_sold', 'created_at', 'updated_at']
    list_editable = ['price', 'stock',]
    prepopulated_fields = {'slug': ('name',)}

    def discount_value(self, obj):
        if obj.discount:
            return obj.discount.value
        else:
            return None

    discount_value.short_description = 'Discount Value'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image',)
    list_editable = ['image']


