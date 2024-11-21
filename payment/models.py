from django.db import models
from userauths.models import User
from core.models import Product, Promotion

import datetime


# Create your models here.
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_type = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    total_price = models.FloatField(default=0)
    status = models.IntegerField(default=1)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    payment = models.OneToOneField(Payment, on_delete=models.RESTRICT, default=0)
    promotion_code = models.ForeignKey(
        Promotion, on_delete=models.RESTRICT, null=True, blank=True
    )
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)


class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=0)
    quantity = models.IntegerField(default=1)


class CanceledOrder(models.Model):
    canceled_order_id = models.AutoField(primary_key=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, default=0)
