from django.contrib import admin
from .models import Payment, Order, OrderItem, CanceledOrder

# Register your models here.


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "payment_id",
        "payment_type",
        "qr_status",
        "cash_status",
        "card_status",
    ]
    exclude = ["card_provider", "expiry_date"]


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_id",
        "user",
        "payment",
        "promotion_code",
        "created_at",
    ]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "order_item_id",
        "order",
        "product",
        "quantity",
    ]


class CanceledOrderAdmin(admin.ModelAdmin):
    list_display = ["canceled_order_id", "order"]


admin.site.register(Payment, PaymentAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CanceledOrder, CanceledOrderAdmin)
