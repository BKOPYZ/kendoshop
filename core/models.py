from django.db import models

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
    armor_color = models.TextField(black=True)
    armor_size = models.IntegerField(null=True)
    
