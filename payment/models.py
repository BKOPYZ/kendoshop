from django.db import models
from userauths.models import User
from core.models import Product, Promotion

import datetime

CARD_PROVIDER = (("debit", "Debit"), ("visa", "Visa"), ("mastercard", "Mastercard"))
PAYMENT_TYPE = (("cash", "Cash"), ("qr", "QrCode"), ("card", "Card"))


# Create your models here.
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True, max_length=9)
    payment_type = models.CharField(choices=PAYMENT_TYPE, max_length=15, default="cash")
    card_provider = models.CharField(
        null=True, blank=True, choices=CARD_PROVIDER, max_length=15
    )
    card_no = models.CharField(null=True, blank=True, max_length=20)
    expiry_date = models.DateField(null=True, blank=True)
    qr_status = models.BooleanField(null=True, blank=True)
    cash_status = models.BooleanField(null=True, blank=True)
    card_status = models.BooleanField(null=True, blank=True)
    total_price = models.FloatField(default=0, max_length=9)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True, max_length=9)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    payment = models.OneToOneField(Payment, on_delete=models.RESTRICT, default=0)
    promotion_code = models.ForeignKey(
        Promotion, on_delete=models.SET_NULL, null=True, blank=True
    )
    address = models.CharField(max_length=255, default="100/100")
    city = models.CharField(max_length=255, default="Parkret")
    province = models.CharField(max_length=255, default="Nonthaburi")
    postal_code = models.CharField(max_length=5, default="11120")
    telephone = models.CharField(max_length=10, default="00000000")
    created_at = models.DateTimeField(default=datetime.datetime.now)
    shipping_status = models.BooleanField(default=False)

    @property
    def is_shipping_successful(self):
        return "Successful" if self.shipping_status else "Has not arrive"


class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True, max_length=9)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=0)
    quantity = models.IntegerField(default=1, max_length=9)


class CanceledOrder(models.Model):
    canceled_order_id = models.AutoField(primary_key=True, max_length=9)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, default=0)
