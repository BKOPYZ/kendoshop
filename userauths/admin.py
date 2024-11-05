from django.contrib import admin
from userauths.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "first_name", "last_name", "telephone"]


# Register your models here.


admin.site.register(User, UserAdmin)
