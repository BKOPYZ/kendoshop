from django.urls import path

from . import views

app_name = "moderate"

urlpatterns = [
    path("home/", views.home_view, name="home"),
    path("product/", views.product_view, name="product"),
    path("product/page/<int:page>/", views.product_view, name="product"),
    path("product/<str:category>/", views.product_view, name="product"),
    path("product/<str:category>/page/<int:page>/", views.product_view, name="product"),
    path(
        "product/<str:category>/<int:product_id>/",
        views.product_detail_view,
        name="product_detail",
    ),
    path("add/product/", views.add_product_view, name="add-product"),
    path(
        "delete/product/",
        views.delete_product_view,
        name="delete-product",
    ),
    path(
        "edit/product/",
        views.update_product_view,
        name="edit-product",
    ),
    path("order/", views.order_view, name="order"),
    path("order/page/<int:page>/", views.order_view, name="order"),
    path("promotion/", views.promotion_view, name="promotion"),
    path("promotion/page/<int:page>/", views.promotion_view, name="promotion"),
    path("promotion/add/", views.add_promotion_view, name="add-promotion"),
    path(
        "promotion/edit/<str:code>/", views.edit_promotion_view, name="edit-promotion"
    ),
    path(
        "promotion/delete/",
        views.delete_promotion_view,
        name="delete-promotion",
    ),
]
