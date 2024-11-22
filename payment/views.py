from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart
from core.models import Product, Promotion
from payment.models import Payment, Order, OrderItem
from cart.models import ShoppingSession, CartItem
from userauths.models import UserAddress, UserPayment
from django.conf import settings

# Create your views here.


def payment_view(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect("core:product")

    if request.method == "POST":
        post = request.POST

        payment_type = post["options"]
        print("payment_type")
        print(payment_type)
        param = {
            "payment_type": payment_type,
        }
        if payment_type == "cash":
            param["cash_status"] = False
        elif payment_type == "qr":
            param["qr_status"] = False
        elif payment_type == "card":
            param.update(request.session[settings.CARD_SESSION_ID])
            param["card_status"] = False

        request.session[settings.PAYMENT_SESSION_ID] = param
        request.session.modified = True

        return redirect("payment:address")

    return render(request, "payment/payment.html")


def select_address_view(request):
    return render(request, "payment/payment_address_option.html")


def new_address_view(request):
    if request.method == "POST":
        post = request.POST

        address = post.get("address")
        city = post.get("city")
        province = post.get("province")
        postal_code = post.get("postal_code")
        telephone = post.get("telephone")

        if request.user.is_authenticated:
            user_address = UserAddress.objects.create(
                user=request.user,
                address=address,
                city=city,
                province=province,
                postal_code=postal_code,
                telephone=telephone,
            )
            user_address.save()

            cart_object = ShoppingSession.objects.get(user=request.user)
            cart_object.delete()

        cart = Cart(request)
        if (payment_data := request.session.get(settings.PAYMENT_SESSION_ID)) is None:
            return redirect("payment:payment")

        payment_data["total_price"] = cart.calculate_total_price
        payment = Payment.objects.create(**payment_data)
        payment.save()

        promotion = None
        if cart.promotion:
            promotion = get_object_or_404(Promotion, code=cart.promotion["code"])
            if promotion.amount < 1:
                cart.unused_promotion()
            else:
                promotion.amount -= 1
                promotion.save()

        user = request.user if request.user.is_authenticated else None
        order = Order.objects.create(
            user=user,
            payment=payment,
            promotion_code=promotion,
            address=address,
            city=city,
            province=province,
            postal_code=postal_code,
            telephone=telephone,
        )
        order.save()
        for product_id, quantity in cart.cart.items():
            product = Product.objects.get(product_id=product_id)
            order_item = OrderItem.objects.create(
                order=order, product=product, quantity=quantity
            )
            product.quantity -= quantity
            product.save()
            order_item.save()

        request.session[settings.CARD_SESSION_ID] = None
        request.session[settings.PAYMENT_SESSION_ID] = {}

        cart.delete_cart()

        return redirect("core:home")
    return render(request, "payment/payment_new_address.html")


def user_address_view(request):
    context = {"addresses": []}
    if request.user.is_authenticated:
        addresses = UserAddress.objects.filter(user=request.user)
        context["addresses"] = addresses

    if request.method == "POST":
        post = request.POST

        cart = Cart(request)
        if cart.promotion:
            promotion = get_object_or_404(Promotion, code=cart.promotion["code"])
            if promotion.amount < 1:
                cart.unused_promotion()
            else:
                promotion.amount -= 1
                promotion.save()

        user_address_id = post.get("address")
        if (payment_data := request.session.get(settings.PAYMENT_SESSION_ID)) is None:
            return redirect("payment:payment")

        payment_data["total_price"] = cart.calculate_total_price

        payment = Payment.objects.create(**payment_data)
        payment.save()

        user_address = UserAddress.objects.get(user_address_id=user_address_id)

        user_address_dict = user_address.to_dict()

        promotion = None
        if cart.promotion:
            promotion = get_object_or_404(Promotion, **cart.promotion)

        order = Order.objects.create(
            user=request.user,
            payment=payment,
            promotion_code=promotion,
            **user_address_dict,
        )
        order.save()

        for product_id, quantity in cart.cart.items():
            product = Product.objects.get(product_id=product_id)
            order_item = OrderItem.objects.create(
                order=order, product=product, quantity=quantity
            )
            product.quantity -= quantity
            product.save()
            order_item.save()

        request.session[settings.CARD_SESSION_ID] = None
        request.session[settings.PAYMENT_SESSION_ID] = {}

        cart.delete_cart()
        cart_object = ShoppingSession.objects.get(user=request.user)
        cart_object.delete()

        return redirect("core:home")

    return render(request, "payment/payment_user_address.html", context)


def new_payment_view(request):
    return render(request, "payment/payment_new_payment.html")


def select_payment_view(request):

    if request.method == "POST":
        post = request.POST

        user_payment_id = post["user_payment_id"]
        user_payment = get_object_or_404(UserPayment, payment_id=user_payment_id)

        request.session[settings.CARD_SESSION_ID] = user_payment.to_dict()

        request.session.modified = True

    return JsonResponse()
