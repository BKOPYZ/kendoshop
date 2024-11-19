from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from core.models import Product
from django.contrib import messages
import math

PRODUCTS_PER_PAGE = 3


# Create your views here.
def index(request):
    return render(request, "core/index.html")


def home_view(request):
    return render(request, "core/home.html")


def product_view(request, category: str | None = None, page: int | None = None):
    if category is None:

        categorize_product = Product.objects.all()
        category = "all product"

    else:

        categorize_product = Product.objects.filter(product_type=category)

    num_products = len(categorize_product)

    num_pages = math.ceil(num_products / PRODUCTS_PER_PAGE)

    page = 1 if page is None else page

    page_products = categorize_product[
        (page - 1) * PRODUCTS_PER_PAGE : max(num_pages, PRODUCTS_PER_PAGE * page)
    ]
    before = range(max(1, page - 2), page)
    after = range(page, min(page + 3, num_pages + 1))

    context = {
        "products": page_products,
        "num_pages": num_pages,
        "page": page,
        "before": before,
        "after": after,
        "category": category.capitalize(),
    }
    return render(request, "core/product.html", context)


def product_detail_view(request, product_id: int, **kwargs):
    try:
        product = Product.objects.get(product_id=product_id)

        size_order = ["xs", "s", "m", "l", "xl"]

        all_same_product = Product.objects.filter(name=product.name)
        context = dict()

        if product.category == "armor":

            all_same_product = sorted(
                all_same_product,
                key=lambda product: size_order.index(product.armor_size),
            )

        elif product.category == "uniform":
            all_same_product = sorted(
                all_same_product,
                key=lambda product: size_order.index(product.uniform_size),
            )
            all_available_color = all_same_product.distinct("uniform_color")
            available_color = Product.objects.filter(
                name=product.name, uniform_size=all_same_product[0].uniform_size
            ).distinct("uniform_color")
            context["available_color"] = available_color
            context["all_available_color"] = all_available_color

        elif product.category == "sword":
            all_same_product = sorted(
                all_same_product,
                key=lambda product: size_order.index(product.sword_length),
            )

        product = all_same_product[0]

        context["product"] = product
        return render(request, "core/product_detail.html", context)

    except Product.DoesNotExist:
        messages.warning(request, "product does not exist")
        return redirect("core:product")
    
def select_same_product(request, product_id: int):
        return redirect("core:product")


def go_back(request):

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
