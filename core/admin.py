from django.contrib import admin
from core.models import (
    Product,
    Promotion,
    # Promotion,
    # Payment,
    # CanceledOrder,
    # CartItem,
    # Order,
    # OrderItem,
    # Session,
    # ShoppingSession,
)

# Register your models here.


class ProductAdmin(admin.ModelAdmin):

    list_display = [
        "product_id",
        "name",
        "product_image",
        "description",
        "price",
        "quantity",
        "product_type",
        "uniform_size",
        "uniform_color",
        "sword_length",
        "armor_size",
        "product_status",
    ]


class PromotionAdmin(admin.ModelAdmin):
    list_display = ["code", "discount", "amount", "end_date"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Promotion, PromotionAdmin)
