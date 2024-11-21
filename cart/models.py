from django.db import models
from userauths.models import User
from core.models import Product
import datetime

# Create your models here.


class ShoppingSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)


class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True, default=0)
    cart = models.ForeignKey(ShoppingSession, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    