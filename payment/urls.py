from django.urls import path

from . import views

app_name = "payment"

urlpatterns = [
    path("", views.payment_view, name="payment"),
    path("address/", views.select_address_view, name="address"),
    path("address/new/", views.new_address_view, name="new-address"),
    path("address/exists/", views.exists_address_view, name="user-address"),
]
