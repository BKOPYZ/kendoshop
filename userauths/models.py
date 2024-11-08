from sys import prefix
from django.db import models
from django.contrib.auth.models import AbstractUser

# from shortuuid.django_fields import ShortUUIDField

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    telephone = models.CharField(max_length=13, null=True)
    user_profile = models.ImageField(upload_to="user/", null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
