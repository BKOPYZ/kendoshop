from sre_constants import SUCCESS
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
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

        all_same_product = Product.objects.filter(
            name=product_name, product_type=product_type
        )
        product = None

        if product_type == "armor":
            armor_size = post.get("size")

            if armor_size is None:

                return JsonResponse({"Success": False})

            product = get_object_or_404(all_same_product, armor_size=armor_size)

        elif product_type == "sword":
            sword_length = post.get("length")

            if sword_length is None:
                return JsonResponse({"Success": False})
            product = get_object_or_404(all_same_product, sword_length=sword_length)
        elif product_type == "uniform":
            uniform_size = post.get("size")
            uniform_color = post.get("color")

            if uniform_size is None or uniform_color is None:

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
        beforePrice = cart.get_total_price
        discount_frac = cart.get_discount_frac
        discount_sale = beforePrice * discount_frac
        total_price = beforePrice - discount_sale
        context = {
            "Quantities": quantity,
            "Product_id": product_id,
            "remove": False,
            "Price": product.price * quantity,
            "TotalPrice": total_price,
            "BeforePrice": beforePrice,
            "DiscountSale": -discount_sale,
        }
        if status == 1:
            messages.error(request, "you can't add more than that bro")
        elif status == 2:
            context["remove"] = True
            context["CartLength"] = len(cart)

        response = JsonResponse(context)
        return response


def remove_item_view(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        post = request.POST
        product_id = post.get("product_id")
        product = get_object_or_404(Product, product_id=product_id)
        cart.delete(product=product)
        beforePrice = cart.get_total_price
        discount_frac = cart.get_discount_frac
        discount_sale = beforePrice * discount_frac
        total_price = beforePrice - discount_sale
        response = JsonResponse(
            {
                "Product_id": product_id,
                "Quantities": len(cart),
                "TotalPrice": total_price,
                "BeforePrice": beforePrice,
                "DiscountSale": -discount_sale,
            }
        )
        return response


def cart_view(request):
    cart = Cart(request)
    products_and_quantities = cart.get_prods()
    if request.method == "POST":
        return redirect("payment:payment")

    return render(request, "cart/cart.html", {"cart_products": products_and_quantities})


def check_coupon_view(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        post = request.POST
        code = post.get("code")
        cart.use_promotion(code)
        beforePrice = cart.get_total_price
        discount_frac = cart.get_discount_frac
        discount_sale = beforePrice * discount_frac
        total_price = beforePrice - discount_sale
        return JsonResponse(
            {
                "Success": True,
                "TotalPrice": total_price,
                "BeforePrice": beforePrice,
                "DiscountSale": -discount_sale,
            }
        )


def clear_coupon_view(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        cart.unused_promotion()
        beforePrice = cart.get_total_price
        discount_frac = cart.get_discount_frac
        discount_sale = beforePrice * discount_frac
        total_price = beforePrice - discount_sale
        return JsonResponse(
            {
                "Success": True,
                "TotalPrice": total_price,
                "BeforePrice": beforePrice,
                "DiscountSale": -discount_sale,
            }
        )
