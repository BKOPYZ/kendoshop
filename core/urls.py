from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("back/", views.go_back, name="back"),
    path("shop/", views.index, name="index"),
    path("home/", views.home_view, name="home"),
    path("product/", views.product_view, name="product"),
    path("product/page/<int:page>", views.product_view, name="product"),
    path("product/<str:category>", views.product_view, name="product"),
    path("product/<str:category>/page/<int:page>", views.product_view, name="product"),
    path(
        "product/<str:category>/<int:product_id>",
        views.product_detail_view,
        name="product_detail",
    ),
]
