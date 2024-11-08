from sys import prefix
from django.db import models
from django.contrib.auth.models import AbstractUser

from pkg_resources import require
from shortuuid.django_fields import ShortUUIDField


def user_directory_path(instance, filename):
    return f"user_{instance.user.user_id}/{filename}"


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
    user_profile = models.ImageField(upload_to=user_directory_path, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class MemberAddress(models.Model):
    member_address_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    road = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)


class MemberPayment(models.Model):
    member_payment_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    account_no = models.CharField(max_length=255)
    expiry_date = models.DateField()
