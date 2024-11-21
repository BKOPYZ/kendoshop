from django.contrib import admin
from cart.models import CartItem, ShoppingSession


# Register your models here.


# class ProductAdmin(admin.ModelAdmin):

#     list_display = [
#         "product_id",
#         "name",
#         "product_image",
#         "description",
#         "price",
#         "quantity",
#         "product_type",
#         "uniform_size",
#         "uniform_color",
#         "sword_length",
#         "armor_size",
#         "product_status",
#     ]


admin.site.register(ShoppingSession)
admin.site.register(CartItem)
