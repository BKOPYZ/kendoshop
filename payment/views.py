from django.shortcuts import redirect, render

from cart.cart import Cart

# Create your views here.


def payment_view(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect("core:product")

    if request.method == "POST":
        pass
        return redirect("payment:address")

    context = dict()

    return render(request, "payment/payment.html")


def select_address_view(request):
    return render(request, "payment/payment_address_option.html")


def new_address_view(request):
    return render(request, "payment/payment_new_address.html")


def exists_address_view(request):
    return render(request, "payment/payment_user_address.html")


def new_payment_view(request):
    return render(request, "payment/payment_new_payment.html")
