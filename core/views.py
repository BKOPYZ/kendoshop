from django.shortcuts import render
from core.models import Product
import math

PRODUCTS_PER_PAGE = 3


# Create your views here.
def index(request):
    return render(request, "core/index.html")


def home(request):
    return render(request, "core/home.html")


def product(request, page: int | None = None):
    all_products = Product.objects.all()

    num_products = len(all_products)

    num_pages = math.ceil(num_products / PRODUCTS_PER_PAGE)

    page = 1 if page is None else page

    page_products = all_products[
        (page - 1) * PRODUCTS_PER_PAGE : max(num_pages, PRODUCTS_PER_PAGE * page)
    ]
    before = range(max(1, page - 2), page)
    after = range(page, min(page + 3, num_pages + 1))

    content = {
        "products": page_products,
        "num_pages": num_pages,
        "page": page,
        "before": before,
        "after": after,
    }
    return render(request, "core/product.html", content)
