from django.contrib import admin
from userauths.models import User


class UserAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        super().delete_model(request, obj)

    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "telephone",
        "is_superuser",
    ]
    exclude = ["password"]


# Register your models here.


admin.site.register(User, UserAdmin)
