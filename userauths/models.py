from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import CharField
from shortuuid.django_fields import ShortUUIDField
from django.core.validators import MinValueValidator, MaxValueValidator

from shortuuid.django_fields import ShortUUIDField
from phonenumber_field.modelfields import PhoneNumberField
from pathlib import Path

CARD_PROVIDER = (("debit", "Debit"), ("visa", "Visa"), ("mastercard", "Mastercard"))


def user_directory_path(instance, filename):
    return f"user/user_{instance.user_id}/{filename}"


# Create your models here.


class User(AbstractUser):

    user_id = ShortUUIDField(
        unique=True,
        length=10,
        max_length=20,
        prefix="user",
        alphabet="abcdefhghijklmnopqrtuvwxyz1234567890",
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=20, default="John")
    last_name = models.CharField(max_length=20, default="Mayer")
    telephone = models.CharField(max_length=13, default="000000000")
    user_privilege = models.IntegerField(
        default=1, validators=[MaxValueValidator(3), MinValueValidator(1)]
    )
    user_profile = models.ImageField(
        upload_to=user_directory_path,
        null=True,
        default="./static/assets/imgs/human.png",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "telephone"]

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        if self.is_superuser:
            self.user_privilege = 3

    def __str__(self):
        return self.username


class UserAddress(models.Model):
    user_address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=5)
    telephone = models.CharField(max_length=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user_address_id",
                    "user",
                    "address",
                    "city",
                    "province",
                    "postal_code",
                    "telephone",
                ],
                name="unique_user_address",
            )
        ]

    def to_dict(self):
        return {
            "address": self.address,
            "city": self.city,
            "province": self.province,
            "postal_code": self.postal_code,
            "telephone": self.telephone,
        }

    def __str__(self):
        return f"{self.address} {self.city} {self.province} {self.postal_code} {self.telephone}"


class UserPayment(models.Model):
    user_payment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_provider = models.CharField(choices=CARD_PROVIDER, max_length=15)
    card_no = models.CharField(max_length=20)
    expiry_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user_payment_id",
                    "user",
                    "card_provider",
                    "card_no",
                    "expiry_date",
                ],
                name="unique_user_payment",
            )
        ]

    def to_dict(self):
        return {
            "card_provider": self.card_provider,
            "card_no": self.card_no,
            "year": self.expiry_date.year,
            "month": self.expiry_date.month,
        }

    def __str__(self):
        return f"xxxx-xxxx-xxxx-x{self.card_no[-3:]}"
