from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("add/", views.add_cart_view, name="add_cart"),
    path("", views.cart_view, name="cart"),
    path("remove", views.remove_item_view, name="remove_cart"),
    path("update/", views.update_item_view, name="update_cart"),
    path("coupon/", views.check_coupon_view, name="check-coupon"),
    path("clear-coupon/", views.clear_coupon_view, name="clear-coupon"),
]
