from django.shortcuts import render
from core.models import Product


# Create your views here.
def index(request):
    return render(request, "core/index.html")


def home(request):
    return render(request, "core/home.html")


def product(request):
    all_product = Product.objects.all()

    content = {"products": all_product}
    return render(request, "core/product.html", content)
