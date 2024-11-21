from email.policy import default
from sys import prefix
from unicodedata import decimal
from django.db import models
from userauths.models import User
from django.utils.html import mark_safe
from shortuuid.django_fields import ShortUUIDField
from django.contrib.sessions.models import Session
import datetime

PRODUCT_SIZE = (
    ("", ""),
    ("xs", "Extra Small"),
    ("s", "Small"),
    ("m", "Medium"),
    ("l", "Large"),
    ("xl", "Extra Large"),
)


PRODUCT_TYPE = (("sword", "Sword"), ("armor", "Armor"), ("uniform", "Uniform"))

SHINAI_SIZE = (
    ("", ""),
    ("28", "28"),
    ("30", "30"),
    ("32", "32"),
    ("34", "34"),
    ("36", "36"),
    ("37", "37"),
    ("37W", "37 Women"),
    ("38", "38"),
    ("38w", "38 Woman"),
    ("39", "39"),
    ("39w", "39 Woman"),
)

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

    uniform_size = models.CharField(
        null=True, max_length=3, blank=True, choices=PRODUCT_SIZE
    )
    uniform_color = models.CharField(null=True, max_length=20, blank=True)

    sword_length = models.CharField(
        null=True, max_length=10, blank=True, choices=SHINAI_SIZE
    )

    armor_size = models.CharField(
        null=True, max_length=3, blank=True, choices=PRODUCT_SIZE
    )

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
        return str(self.product_id)


class Promotion(models.Model):
    code = models.CharField(max_length=255, primary_key=True, default="HAPPY")
    discount = models.FloatField(default=0.15)
    amount = models.IntegerField(default=1000)
    end_date = models.DateField(default=datetime.datetime.now, blank=True, null=True)

