from django.contrib import admin

from .models import Product, Cart, Order, ShippingAddress, Image

# Register your models here.

class ImageInline(admin.StackedInline):
    model = Image

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline
    ]



admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(ShippingAddress)