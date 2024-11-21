from venv import create
from django.contrib import admin
from cart.models import CartItem, ShoppingSession


class ShoppingSessionAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at", "promotion"]


class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart_item_id", "cart", "product", "quantity"]


admin.site.register(ShoppingSession, ShoppingSessionAdmin)
admin.site.register(CartItem, CartItemAdmin)
