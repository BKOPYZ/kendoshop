from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("shop/", views.index, name="index"),
]
