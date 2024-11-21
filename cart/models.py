from django.db import models
from userauths.models import User
from core.models import Product, Promotion

import datetime

# Create your models here.


class ShoppingSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    promotion = models.ForeignKey(
        Promotion, null=True, blank=True, on_delete=models.RESTRICT
    )


class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(ShoppingSession, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
