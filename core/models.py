from email.policy import default
from sys import prefix
from unicodedata import decimal
from django.db import models
from userauths.models import User
from django.utils.html import mark_safe
from shortuuid.django_fields import ShortUUIDField
from django.contrib.sessions.models import Session
import datetime

PRODUCT_TYPE = (("sword", "Sword"), ("armor", "Armor"), ("uniform", "Uniform"))

STATUS = (
    ("available", "Available"),
    ("not available", "Not Available"),
    ("out of stock", "Out of Stock"),
)

RATING = (
    (0, "☆☆☆☆☆"),
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)
# Create your models here.

# TODO: handle admin and product transaction


class Product(models.Model):
    _image_width: int = 50
    _image_height: int = 50
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="name of a product")
    description = models.TextField(null=True, blank=True, default="This is a product")
    image = models.ImageField(upload_to="product/", default="product.png")
    price = models.DecimalField(max_digits=99999999, decimal_places=2, default=0.0)
    quantity = models.IntegerField(default=0)

    product_type = models.CharField(
        choices=PRODUCT_TYPE, max_length=20, default="sword"
    )

    uniform_size = models.IntegerField(null=True, blank=True)

    sword_length = models.IntegerField(null=True, blank=True)

    armor_color = models.TextField(blank=True, null=True)
    armor_size = models.IntegerField(null=True, blank=True)

    product_status = models.CharField(
        choices=STATUS, max_length=20, default="available"
    )

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe(
            f'<img src="{self.image.url}" width={self._image_width} height={self._image_height} />'
        )

    def __str__(self):
        return self.name


class ShoppingSession(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)


class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True, default=0)
    session = models.ForeignKey(ShoppingSession, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Promotion(models.Model):
    code = models.CharField(max_length=255, primary_key=True, default="HAPPY")
    discount = models.FloatField(default=0.15)
    amount = models.IntegerField(default=1000)
    end_date = models.DateField(default=datetime.datetime.now, blank=True, null=True)


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True, default=0)
    payment_type = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    total_price = models.FloatField(default=0)
    status = models.IntegerField(default=1)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True, default=0)
    member = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    payment = models.OneToOneField(Payment, on_delete=models.RESTRICT, default=0)
    promotion_code = models.ForeignKey(
        Promotion, on_delete=models.RESTRICT, null=True, blank=True
    )
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)


class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True, default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=0)
    quantity = models.IntegerField(default=1)


class CanceledOrder(models.Model):
    canceled_order_id = models.AutoField(primary_key=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, default=0)
