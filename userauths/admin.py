from django.contrib import admin
from userauths.models import User


class UserAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        print("request")
        print(request)
        print("obj")
        print(obj)
        print("form")
        print(form)
        print("change")
        print(change)
        print("SAVE MODEL DETECTED")

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        print("DELETE MODEL DETECTED")

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
