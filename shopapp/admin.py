from django.contrib import admin

# Register your models here.
from .models import Product, Cart, CartItem


admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
