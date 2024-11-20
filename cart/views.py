from sre_constants import SUCCESS
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
        product_name = post.get("product_name")
        product_type = post.get("product_type")
        product_qty = int(post.get("product_qty"))
        print("----------")
        print(product_name)
        print(product_type)
        print(product_qty)
        print("----------")

        all_same_product = Product.objects.filter(
            name=product_name, product_type=product_type
        )
        product = None

        if product_type == "armor":
            armor_size = post.get("size")

            if armor_size is None:
                print("armor length None")
                
                return JsonResponse({"Success": False})

            product = get_object_or_404(all_same_product, armor_size=armor_size)

        elif product_type == "sword":
            sword_length = post.get("length")

            if sword_length is None:
                print("sword length None")
                return JsonResponse({"Success": False})
            product = get_object_or_404(all_same_product, sword_length=sword_length)
        elif product_type == "uniform":
            uniform_size = post.get("size")
            uniform_color = post.get("color")

            if uniform_size is None or uniform_color is None:
                print("uniform length None")
                
                return JsonResponse({"Success": False})
            product = get_object_or_404(
                all_same_product, uniform_size=uniform_size, uniform_color=uniform_color
            )

        if product.quantity <= 0:
            return JsonResponse({"Success": False})

        cart.add(product=product, quantity=product_qty)

        cart_quantity = len(cart)

        response = JsonResponse(
            {"Product Name: ": product.name, "Quantity": cart_quantity, "Success": True}
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
