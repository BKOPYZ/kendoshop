from django.contrib import admin
from userauths.models import User, UserPayment, UserAddress


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


class UserPaymentAdmin(admin.ModelAdmin):
    list_display = [
        "member_payment_id",
        "member",
        "payment_type",
        "provider",
        "expiry_date",
    ]

    exclude = ["account_no"]


class UserAddressAdmin(admin.ModelAdmin):
    list_display = [
        "member_address_id",
        "member",
        "address",
        "road",
        "city",
        "province",
        "postal_code",
        "telephone",
    ]


admin.site.register(User, UserAdmin)
admin.site.register(UserPayment, UserPaymentAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
