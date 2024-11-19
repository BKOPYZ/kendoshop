from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from core.models import Product
from .cart import Cart

# Create your views here.


def add_cart_view(request):
    cart = Cart(request)

    if request.POST.get("action") == "post":
        post = request.POST
        product_id = int(post.get("product_id"))
        product_qty = int(post.get("product_qty"))

        product = get_object_or_404(Product, product_id=product_id)

        cart.add(product=product, quantity=product_qty)

        cart_quantity = len(cart)

        response = JsonResponse(
            {"Product Name: ": product.name, "Quantity": cart_quantity}
        )
        return response


def update_item_view(
    request,
):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        post = request.POST
        product_id = post.get("product_id")
        difference = post.get("difference")
        product = get_object_or_404(Product, product_id=product_id)
        status, quantity = cart.add(product=product, quantity=difference)
        context = {"Quantities": quantity, "Product_id": product_id, "remove": False}
        if status == 1:
            messages.error(request, "you can't add more than that bro")
        elif status == 2:
            context["remove"] = True

        response = JsonResponse(context)
        return response


def remove_item_view(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        post = request.POST
        product_id = post.get("product_id")
        product = get_object_or_404(Product, product_id=product_id)
        cart.delete(product=product)
        response = JsonResponse({"Product_id": product_id, "Quantities": len(cart)})
        return response


def cart_view(request):
    cart = Cart(request)
    products_and_quantities = cart.get_prods()
    return render(request, "cart/cart.html", {"cart_products": products_and_quantities})
