from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from pkg_resources import require
from userauths.models import User
from django.core.files import File
from django.contrib.auth.decorators import login_required, user_passes_test
from payment.models import Order, OrderItem, Payment, CanceledOrder
from cart.cart import Cart
from django.db.models.expressions import RawSQL
import os


def register_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    context = dict()
    if request.method == "POST" and request.POST.get("submit", False):
        post = request.POST
        first_name = post.get("firstname", None)
        last_name = post.get("lastname", None)
        telephone = post.get("telephone")
        username = post.get("username")
        email = post.get("email")
        password = post.get("password")
        confirm_password = post.get("confirm_password")

        context["telephone"] = telephone
        context["username"] = username
        context["email"] = email

        is_valid = True

        if User.objects.filter(username=username).exists():
            messages.error(request, "error exists username")
            is_valid = False

        if password != confirm_password:
            messages.error(request, "error password not the same")
            is_valid = False

        if is_valid:
            try:
                new_user = User.objects.create(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    telephone=telephone,
                )
                user_profile = request.FILES.get("user_profile", None)
                context["userprofile"] = user_profile

                is_profile_None = False

                if user_profile is None:

                    user_profile = "/user/user_no_img/human.png"
                    is_profile_None = True

                new_user.user_profile = user_profile
                if not is_profile_None:
                    new_user.user_profile.save(
                        "user_profile.png",
                        File(user_profile),
                    )
                new_user.set_password(password)
                # insert into user
                new_user.save()

                messages.info(request, "Thanks for registering. You are now logged in.")
                new_user = authenticate(
                    username=email,
                    password=password,
                )
                login(request, new_user)
                cart = Cart(request)
                cart.load_from_database(cart.cart)
                return redirect("core:home")
            except Exception as e:
                print(e)
                messages.error(request, e)
    return render(request, "userauths/sign-up.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    context = dict()
    if request.method == "POST":
        post = request.POST
        email = post.get("email")
        password = post.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "email does not exist")
        else:
            user = authenticate(request, email=email, password=password)

            if user is not None:

                login(request, user)
                messages.success(request, "you are login")
                cart = Cart(request)
                cart.load_from_database(cart.cart)
                return redirect("core:home")
            else:
                messages.error(
                    request, "user doesnot exist or password does not correct"
                )

    return render(request, "userauths/login.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "You have logout")
    return redirect("userauths:login")


@login_required(login_url="userauths:login")
def profile_view(request):
    context = dict()
    orders = Order.objects.filter(
        order_id__in=RawSQL(
            f"select payment_order.order_id from payment_order left join payment_canceledorder on payment_order.order_id = payment_canceledorder.order_id where user_id = %s and payment_canceledorder.order_id is null",
            (request.user.id,),
        )
    )
    order_payment_orderItems = []
    for order in orders:
        payment = Payment.objects.get(order=order)
        order_items = OrderItem.objects.filter(order=order)
        order_payment_orderItems.append((order, payment, order_items))

    context["order_payment_orderItems"] = order_payment_orderItems

    return render(request, "userauths/profile.html", context)


@login_required(redirect_field_name="userauths:login")
def edit_profile_view(request):

    context = dict()

    if request.method == "POST":
        post = request.POST

        first_name = post.get("firstname")
        last_name = post.get("lastname")
        email = post.get("email")

        context["firstname"] = first_name
        context["lastname"] = last_name
        context["email"] = email

        user = User.objects.filter(email=email)

        if user.exists() and user[0].user_id != request.user.user_id:
            context["email"] = ""
            messages.error(request, "this email has been used")

        else:
            user = User.objects.get(user_id=request.user.user_id)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user_profile = request.FILES.get("user_profile", None)
            context["userprofile"] = user_profile

            if user_profile is not None:
                user.user_profile = user_profile
                user.user_profile.save(
                    "user_profile.png",
                    File(user_profile),
                )
            user.save()
            messages.success(request, "success")
            return redirect("userauths:profile")

    return render(request, "userauths/edit_profile.html", {})


def cancel_order_view(request):
    if request.method == "POST":
        post = request.POST
        order_id = post["order_id"]
        order = Order.objects.get(order_id=order_id)
        canceled_order = CanceledOrder.objects.create(order=order)
        canceled_order.save()
        order_items = OrderItem.objects.filter(order=order)
        for order_item in order_items:
            product = order_item.product
            product.quantity += order_item.quantity
            product.save()

        return JsonResponse({"Success": True, "order_id": order_id})
    return redirect("core:home")
