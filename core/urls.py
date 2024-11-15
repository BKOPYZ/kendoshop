from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("shop/", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("product/", views.product, name="product"),
    path("product/page/<int:page>", views.product, name="product"),
]
