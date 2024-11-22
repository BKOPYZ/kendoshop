from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart
from core.models import Product, Promotion
from payment.models import Payment, Order, OrderItem
from cart.models import ShoppingSession, CartItem
from userauths.models import UserAddress, UserPayment
from django.conf import settings
from django.contrib import messages
import datetime

# Create your views here.


def payment_view(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect("core:product")
    context = dict()

    if request.user.is_authenticated:
        user_payment = UserPayment.objects.filter(user=request.user)
        context["user_payment"] = user_payment

    if request.method == "POST":
        post = request.POST

        payment_type = post["options"]
        print("payment_type")
        print(payment_type)
        param = {
            "payment_type": payment_type,
            "total_price": cart.calculate_total_price,
        }
        if payment_type == "cash":
            param["cash_status"] = False
        elif payment_type == "qr":
            param["qr_status"] = False
        elif payment_type == "card":
            if request.user.is_authenticated:
                param.update(request.session[settings.CARD_SESSION_ID])
            else:
                card_no = post["card_no"]
                if card_no[0] in ("5", "2"):
                    card_provider = "mastercard"
                elif card_no[0] == "4":
                    card_provider = "visa"
                else:
                    messages.error(request, "invalid card number")
                    return
                try:
                    month = int(post["month"])
                    year = int(post["year"])
                except:
                    messages.error(request, "invalid montha nad year")

                    return render(request, "payment/payment.html")
                code = post["code"]
                name = post["name"]
                expiry_date = datetime.datetime(year=year, month=month)
                param.update(
                    {
                        "card_no": card_no,
                        "expiry_date": expiry_date,
                        "card_provider": card_provider,
                    }
                )
            param["card_status"] = False

        request.session[settings.PAYMENT_SESSION_ID] = param
        request.session.modified = True

        return redirect("payment:address")

    return render(request, "payment/payment.html", context)


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

        payment = Payment.objects.create(**payment_data)
        payment.save()

        promotion = None
        if cart.promotion:
            promotion = get_object_or_404(Promotion, **cart.promotion)

        order = Order.objects.create(
            user=request.user,
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
            order_item.save()
        request.session[settings.CARD_SESSION_ID] = None
        request.session[settings.PAYMENT_SESSION_ID] = {}

        cart.delte_cart()

        return redirect("core:home")
    return render(request, "payment/payment_new_address.html")


def exists_address_view(request):
    context = {"addresses": []}

    if request.user.is_authenticated:
        addresses = UserAddress.objects.filter(user=request.user)
        context["addresses"] = addresses

    if request.method == "POST":
        post = request.POST

        user_address_id = post.get("address_id")
        cart = Cart(request)
        if (payment_data := request.session.get(settings.PAYMENT_SESSION_ID)) is None:
            return redirect("payment:payment")

        payment = Payment.objects.create(**payment_data)
        payment.save()

        user_address = UserAddress.objects.get(user_address_id=user_address_id)

        user_address_dict = user_address.__dict__

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
            product.quantity -= quantity
            product.save()
            order_item = OrderItem.objects.create(
                order=order, product=product, quantity=quantity
            )
            order_item.save()

        request.session[settings.CARD_SESSION_ID] = None
        request.session[settings.PAYMENT_SESSION_ID] = {}

        cart.delte_cart()
        cart_object = ShoppingSession.objects.get(user=request.user)
        cart_object.delete()

        return redirect("core:home")

    return render(request, "payment/payment_user_address.html")


def new_payment_view(request):
    if not request.user.is_authenticated:
        redirect("payment:payment")

    if request.method == "POST":
        post = request.POST
        card_provider = post["card_provider"]
        card_no = post["card_no"]
        try:
            month = post["month"]
            year = post["year"]
        except:
            messages.error(request, "please enter month in int and year in int")
            return render(request, "payment/payment_new_payment.html")
        expiry_date = datetime.datetime(int(year), int(month))

        user_address = UserAddress.objects.create(
            card_provider=card_provider, card_no=card_no, expiry_date=expiry_date
        )
        user_address.save()

        return redirect("payment:payment")

    return render(request, "payment/payment_new_payment.html")


def select_payment_view(request):

    if request.method == "POST":
        post = request.POST

        user_payment_id = post["user_payment_id"]
        UserPayment = get_object_or_404(UserPayment, payment_id=user_payment_id)

        request.session[settings.CARD_SESSION_ID] = UserPayment.__dict__

        request.session.modified = True

    return JsonResponse()
