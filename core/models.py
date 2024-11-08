from django.db import models
from userauths.models import User
from django.utils.html import mark_safe


def user_directory_path(instance, filename):
    return f"user_{instance.User.id}/{filename}"


# Create your models here.

# TODO: handle admin and product transaction


class Product(models.Model):
    _image_width: int = 50
    _image_height: int = 50
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="product")
    price = models.FloatField()
    quantity = models.IntegerField()
    product_type = models.CharField(max_length=20)
    uniform_size = models.IntegerField(null=True)
    sword_length = models.IntegerField(null=True)
    armor_color = models.TextField(blank=True)
    armor_size = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe(
            f'<img src="{self.image}>" width="{self._image_width} height="{self._image_height}" />'
        )

    def __str__(self):
        return self.name


class ShoppingSession(models.Model):
    session_id = models.UUIDField(unique=True, primary_key=True)
    user_id = models.ForeignKey(to=User, to_field="id", on_delete=models.CASCADE)


class CartItem(models.Model):
    cart_item_id = models.UUIDField(unique=True, primary_key=True)
    # session_id
    # product_id
    quantity = models.IntegerField()
