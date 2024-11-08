from sys import prefix
from unicodedata import decimal
from django.db import models
from userauths.models import User
from django.utils.html import mark_safe
from shortuuid.django_fields import ShortUUIDField

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
    product_id = ShortUUIDField(
        unique=True,
        length=10,
        max_length=20,
        prefix="prod",
        alphabet="abcdefhghijklmnopqrtuvwxyz1234567890",
    )
    name = models.CharField(max_length=100, default="name of a product")
    description = models.TextField(null=True, blank=True, default="This is a product")
    image = models.ImageField(upload_to="product/", default="product.png")
    price = models.DecimalField(max_digits=99999999, decimal_places=2, default=0.0)
    quantity = models.IntegerField(default=0)

    product_type = models.CharField(max_length=20, default="sword")

    uniform_size = models.IntegerField(null=True, default=30)

    sword_length = models.IntegerField(null=True, default=30)

    armor_color = models.TextField(blank=True, default="red")
    armor_size = models.IntegerField(null=True, default=30)

    product_status = models.CharField(
        choices=STATUS, max_length=20, default="available"
    )

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe(
            f'<img src="{self.image.url}>" width="{self._image_width} height="{self._image_height}" />'
        )

    def __str__(self):
        return self.name


class Order(models.Model):
    pass


class OrderItem(models.Model):
    pass
