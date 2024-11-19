from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("cart/add/", views.add_cart_view, name="add_cart"),
    path("cart/", views.cart_view, name="cart"),
    path("", views.remove_item_view, name="remove_cart"),
    path("cart/update/", views.update_item_view, name="update_cart"),
]
