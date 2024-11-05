from django.db import models
from userauths.models import User
# Create your models here.


class Product(models.Model):
    product_id = models.UUIDField(unique=True, primary_key=True)
    name = models.TextField()
    description = models.TextField()
    image = models.ImageField()
    price = models.FloatField()
    quantity = models.IntegerField()
    product_type = models.TextField()
    uniform_size = models.IntegerField(null=True)
    sword_length = models.IntegerField(null=True)
    armor_color = models.TextField(blank=True)
    armor_size = models.IntegerField(null=True)


class ShoppingSession(models.Model):
    session_id = models.UUIDField(unique=True, primary_key=True)
    # TODO: handle the foreign key
    # member_username = models.ForeignKey(to=User.username )
class CartItem(models.Model):
    cart_item_id = models.UUIDField(unique=True, primary_key=True)
    #session_id
    #product_id
    quantity = models.IntegerField()
    
