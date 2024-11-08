from sys import prefix
from unicodedata import decimal
from django.db import models
from userauths.models import User
from django.utils.html import mark_safe
from shortuuid.django_fields import ShortUUIDField
from django.contrib.sessions.models import Session

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


class ShoppingSession(models.Model):
    # Use Django's session ID to associate with a user's session directly
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    session = models.ForeignKey(ShoppingSession, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    product_type = models.CharField(max_length=255)
    size_uniform = models.IntegerField(null=True, blank=True)
    length_sword = models.IntegerField(null=True, blank=True)
    color_armor = models.CharField(max_length=255, null=True, blank=True)
    size_armor = models.IntegerField(null=True, blank=True)

class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    session = models.ForeignKey('ShoppingSession', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class ShoppingSession(models.Model):
    session_id = models.AutoField(primary_key=True)
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CanceledOrder(models.Model):
    canceled_order_id = models.AutoField(primary_key=True)
    order = models.OneToOneField('Order', on_delete=models.CASCADE)

class Promotion(models.Model):
    code = models.CharField(max_length=255, primary_key=True)
    discount = models.IntegerField()
    amount = models.IntegerField()
    end_date = models.DateField()

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    payment = models.OneToOneField('Payment', on_delete=models.RESTRICT)
    promotion_code = models.ForeignKey(Promotion, on_delete=models.RESTRICT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_type = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    total_price = models.FloatField()
    status = models.IntegerField()