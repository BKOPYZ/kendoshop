from sys import prefix
from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField

from pkg_resources import require
from shortuuid.django_fields import ShortUUIDField

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
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    telephone = models.CharField(max_length=13, null=True)
    user_profile = models.ImageField(
        upload_to=user_directory_path,
        null=True,
        default="../static/assets/imgs/human.png",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class UserAddress(models.Model):
    user_address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)

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
    card_provider = models.CharField(
        null=True, blank=True, choices=CARD_PROVIDER, max_length=15
    )
    card_no = models.CharField(null=True, blank=True, max_length=20)
    expiry_date = models.DateField(null=True, blank=True)

    def to_dict(self):
        return {
            "payment_type": self.payment_type,
            "provider": self.provider,
            "account_no": self.account_no,
            "expiry_date": self.expiry_date,
        }

    def __str__(self):
        return f"xxxx-xxxx-xxxx-x{self.card_no[-3:]}"
