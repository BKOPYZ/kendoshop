from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("shop/", views.index, name="index"),
    path("home/", views.home_view, name="home"),
    path("product/", views.product_view, name="product"),
    path("product/page/<int:page>", views.product_view, name="product"),
    path("product/<str:category>", views.product_view, name="product"),
    path("product/<str:category>/page/<int:page>", views.product_view, name="product"),
]
