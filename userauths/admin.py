from django.contrib import admin
from userauths.models import User, UserPayment, UserAddress


class UserAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.is_superuser = int(obj.user_privilege) > 2
        obj.is_admin = int(obj.user_privilege) > 2
        obj.is_staff = int(obj.user_privilege) > 1
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        super().delete_model(request, obj)

    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "telephone",
        "is_staff",
        "is_superuser",
    ]
    exclude = ["password"]


# Register your models here.


class UserPaymentAdmin(admin.ModelAdmin):
    list_display = [
        "user_payment_id",
        "user",
        "card_provider",
        "expiry_date",
    ]

    exclude = ["card_no"]


class UserAddressAdmin(admin.ModelAdmin):
    list_display = [
        "user_address_id",
        "user",
        "address",
        "city",
        "province",
        "postal_code",
        "telephone",
    ]


admin.site.register(User, UserAdmin)
admin.site.register(UserPayment, UserPaymentAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
filter
