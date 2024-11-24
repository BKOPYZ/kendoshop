from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from cart.cart import Cart
from core.models import Product
from django.contrib import messages
from django.db.models import Count
import math
from userauths.models import UserAddress

PRODUCTS_PER_PAGE = 5


def home_view(request):
    return render(request, "core/home.html")


def product_view(request, category: str | None = None, page: int | None = None):
    if product_name := request.GET.get("search"):
        categorize_product = Product.objects.raw(
            f"Select * from core_product where name like '%{product_name}%' group by name"
        )
        category = product_name

    elif category is None:

        categorize_product = Product.objects.raw(
            "Select * from core_product group by name"
        )
        category = "all product"

    else:
        categorize_product = Product.objects.raw(
            f"Select * from core_product where product_type = '{category}' group by name"
        )

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

    context = dict()
    try:
        product = Product.objects.get(product_id=product_id)

        size_order = [None, "xs", "s", "m", "l", "xl"]

        all_same_product = Product.objects.filter(name=product.name)

        if product.product_type == "armor":
            size_quantity_price = [
                (product.armor_size, product.quantity, product.price)
                for product in all_same_product
            ]
            size_quantity_price = sorted(
                size_quantity_price, key=lambda product: size_order.index(product[0])
            )
            context["size_quantity_price"] = size_quantity_price

        elif product.product_type == "uniform":
            distinct_color = set()
            distinct_size = set()
            size_color_quantity_price = []

            for product in all_same_product:
                size_color_quantity_price.append(
                    (
                        product.uniform_size,
                        product.uniform_color,
                        product.quantity,
                        product.price,
                    )
                )
                distinct_color.add(product.uniform_color)
                distinct_size.add(product.uniform_size)

            distinct_size = sorted(
                distinct_size, key=lambda size: size_order.index(size)
            )

            context["size_color_quantity_price"] = size_color_quantity_price
            context["distinct_color"] = distinct_color
            context["distinct_size"] = distinct_size

        elif product.product_type == "sword":
            length_quantity_price = [
                (product.sword_length, product.quantity, product.price)
                for product in all_same_product
            ]
            length_quantity_price = sorted(
                length_quantity_price, key=lambda product: product[0]
            )
            context["length_quantity_price"] = length_quantity_price

        context["product"] = product
        return render(request, "core/product_detail.html", context)

    except Product.DoesNotExist:
        messages.warning(request, "product does not exist")
        return redirect("core:product")


def go_back(request):

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
