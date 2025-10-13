from django.contrib import admin
from .models import User, Vendor, Item, Order, OrderItem, Cart, CartItem

# Register your models here.

admin.site.register(User)
admin.site.register(Vendor)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)