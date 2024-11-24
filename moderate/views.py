from urllib import request
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from core.models import Product, Promotion
from payment.models import Order, Payment, OrderItem
import math
from django.core.files import File
from core.views import PRODUCTS_PER_PAGE
from django.contrib import messages

ORDERS_PER_PAGE = 3
PROMOTIONS_PER_PAGE = 10


@login_required(login_url="userauths:login")
def order_view(request, page: int | None = None):

    if request.user.user_privilege < 2:
        return redirect("core:home")

    all_order_cancelordered = Order.objects.raw(
        "select * from payment_order left join payment_canceledorder on payment_order.order_id = payment_canceledorder.order_id"
    )

    order_payment_orderItems = []
    for order in all_order_cancelordered:
        payment = Payment.objects.get(order=order)
        order_items = OrderItem.objects.filter(order=order)
        order_payment_orderItems.append((order, payment, order_items))

    num_order = len(all_order_cancelordered)

    num_pages = math.ceil(num_order / ORDERS_PER_PAGE)

    page = 1 if page is None else page

    page_orders = order_payment_orderItems[
        (page - 1) * ORDERS_PER_PAGE : max(num_pages, ORDERS_PER_PAGE * page)
    ]
    before = range(max(1, page - 2), page)
    after = range(page, min(page + 3, num_pages + 1))

    context = {
        "order_payment_orderItems": page_orders,
        "num_pages": num_pages,
        "page": page,
        "before": before,
        "after": after,
    }
    return render(request, "moderate/order.html", context)


@login_required(login_url="userauths:login")
def home_view(request):
    if request.user.user_privilege < 2:
        return redirect("core:home")
    return render(request, "moderate/home.html")


@login_required(login_url="userauths:login")
def product_view(request, category: str | None = None, page: int | None = None):
    if request.user.user_privilege < 2:
        return redirect("core:home")

    if category is None:

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
    return render(request, "moderate/product.html", context)


@login_required(login_url="userauths:login")
def product_detail_view(request, product_id: int, **kwargs):

    context = dict()
    if request.user.user_privilege < 2:
        return redirect("core:home")
    try:
        product = Product.objects.get(product_id=product_id)

        size_order = [None, "xs", "s", "m", "l", "xl"]

        all_same_product = Product.objects.filter(name=product.name)

        if product.product_type == "armor":
            id_size_quantity_price = [
                (
                    product.product_id,
                    product.armor_size,
                    product.quantity,
                    product.price,
                )
                for product in all_same_product
            ]
            id_size_quantity_price = sorted(
                id_size_quantity_price, key=lambda product: size_order.index(product[1])
            )
            context["id_size_quantity_price"] = id_size_quantity_price

        elif product.product_type == "uniform":
            id_size_color_quantity_price = []

            for product in all_same_product:
                id_size_color_quantity_price.append(
                    (
                        product.product_id,
                        product.uniform_size,
                        product.uniform_color,
                        product.quantity,
                        product.price,
                    )
                )
                id_size_color_quantity_price = sorted(
                    id_size_color_quantity_price,
                    key=lambda product: size_order.index(product[1]),
                )

            context["id_size_color_quantity_price"] = id_size_color_quantity_price

        elif product.product_type == "sword":

            id_length_quantity_price = [
                (
                    product.product_id,
                    product.sword_length,
                    product.quantity,
                    product.price,
                )
                for product in all_same_product
            ]
            id_length_quantity_price = sorted(
                id_length_quantity_price, key=lambda product: product[0]
            )
            context["id_length_quantity_price"] = id_length_quantity_price

        context["product"] = product
        return render(request, "moderate/product_detail.html", context)

    except Product.DoesNotExist:
        messages.warning(request, "product does not exist")
        return redirect("moderate:product")


@login_required(login_url="userauths:login")
def add_product_view(request, **kwargs):
    if request.user.user_privilege < 2:
        return redirect("core:home")

    if request.method == "POST":
        post = request.POST
        name = post.get("name")
        description = post.get("description")
        price = float(post.get("price"))
        quantity = int(post.get("quantity"))
        product_type = post.get("product_type")
        if product_type == "Select type":
            messages.error(request, f"[ERROR]: please select product type")
            return render(request, "moderate/add_product.html")

        params = {
            "name": name,
            "description": description,
            "price": price,
            "quantity": quantity,
            "product_type": product_type,
        }
        if product_type == "sword":
            sword_length = post.get("sword_length")
            if sword_length == "Sword Length":
                messages.error(request, f"[ERROR]: please pick one of the sword length")
                return render(request, "moderate/add_product.html")

            params["sword_length"] = sword_length
        elif product_type == "armor":
            armor_size = post.get("armor_size")
            if armor_size == "Armor Size":
                messages.error(request, f"[ERROR]: please pick one of the armor size")
                return render(request, "moderate/add_product.html")
            params["armor_size"] = armor_size
        elif product_type == "uniform":
            uniform_color = post.get("uniform_color")
            uniform_size = post.get("uniform_size")
            if uniform_size == "Uniform Size" or uniform_color is None:
                messages.error(
                    request,
                    f"[ERROR]: please pick one of the uniform size or uniform color",
                )
                return render(request, "moderate/add_product.html")
            params.update(
                {
                    "uniform_color": uniform_color,
                    "uniform_size": uniform_size,
                }
            )
        try:
            product = Product.objects.create(**params)
            image = request.FILES.get("image", None)

            is_image_none = False

            if image is None:

                image = "/user/user_no_img/human.png"
                is_image_none = True

            product.image = image
            if not is_image_none:
                product.user_profile.save(
                    "product_404.png",
                    File(image),
                )
            product.save()
            messages.success(request, "create product successfully")
            return redirect("moderate:product")
        except Exception as e:
            messages.error(request, f"[ERROR]: {e}")

    return render(request, "moderate/add_product.html")


@login_required(login_url="userauths:login")
def delete_product_view(request):
    if request.user.user_privilege < 2:
        return redirect("core:home")

    if request.method != "POST":
        return redirect("moderate:product")

    try:
        post = request.POST
        product_id = post["product_id"]
        product = Product.objects.get(product_id=product_id)
        product.delete()
        return JsonResponse({"Success": True, "Message": "[INFO]: successfully delete"})
    except Exception as e:
        print(e)
        return JsonResponse({"Success": False, "Message": f"[ERROR]: {e}"})


@login_required(login_url="userauths:login")
def update_product_view(request):
    if request.user.user_privilege < 2:
        return redirect("core:home")

    if request.method != "POST":
        return redirect("moderate:product")

    try:
        post = request.POST

        quantity = int(post["product_quantity"])
        price = float(post["product_price"])
        product_type = post["product_type"]
        product_id = post["product_id"]
        product = Product.objects.get(product_id=product_id)
        assert product_type == product.product_type
        product.quantity = quantity
        product.price = price
        product.save()
        return JsonResponse(
            {
                "Success": True,
                "Quantity": quantity,
                "Price": price,
                "Product_id": product_id,
                "Message": "[INFO]: successfully edited",
            }
        )

    except Exception as e:
        messages.error(request, f"[ERROR]: {e}")
        return JsonResponse(
            {
                "Success": False,
                "Message": f"[ERROR]: {e}",
            }
        )


@login_required(login_url="userauths:login")
def promotion_view(request, page: int | None = None):

    if request.user.user_privilege < 2:
        return redirect("core:home")

    all_promotion = Promotion.objects.all()

    num_order = len(all_promotion)

    num_pages = math.ceil(num_order / ORDERS_PER_PAGE)

    page = 1 if page is None else page

    page_promotion = all_promotion[
        (page - 1) * ORDERS_PER_PAGE : max(num_pages, ORDERS_PER_PAGE * page)
    ]
    before = range(max(1, page - 2), page)
    after = range(page, min(page + 3, num_pages + 1))

    context = {
        "promotions": page_promotion,
        "num_pages": num_pages,
        "page": page,
        "before": before,
        "after": after,
    }
    return render(request, "moderate/promotion.html", context)


@login_required(login_url="userauths:login")
def edit_promotion_view(request, code: str | None = None):

    if request.user.user_privilege < 2:
        return redirect("core:home")
    context = dict()
    try:
        edit_promotion = Promotion.objects.get(code=code)
    except Exception as e:
        messages.error(request, f"[ERROR]: {e}")
        return redirect("moderate:promotion")

    context["promotion"] = edit_promotion

    if request.method == "POST":
        post = request.POST
        try:
            edit_promotion.code = post["code"]
            edit_promotion.amount = post["amount"]
            edit_promotion.discount = post["discount"]
            edit_promotion.end_date = post["end_date"]
            edit_promotion.save()
            messages.success(request, f"[INFO]: successfully modify promotion")
            return redirect("moderate:promotion")
        except Exception as e:
            messages.error(request, f"[Error]: {e}")

    return render(request, "moderate/edit_promotion.html", context)


# Create your views here.
@login_required(login_url="userauths:login")
def add_promotion_view(request):
    if request.user.user_privilege < 2:
        return redirect("core:home")
    if request.method == "POST":
        post = request.POST
        code = post["code"]
        amount = post["amount"]
        discount = post["discount"]
        end_date = post["end_date"]

        try:
            promotion = Promotion.objects.create(
                code=code, amount=amount, discount=discount, end_date=end_date
            )
            promotion.save()
            messages.success(request, f"[INFO]: successfully create promotion")

            return redirect("moderate:promotion")

        except Exception as e:
            messages.error(request, f"[Error]: {e}")
    return render(request, "moderate/add_promotion.html")


@login_required(login_url="userauths:login")
def delete_promotion_view(request, code):
    if request.user.user_privilege < 2:
        return redirect("core:home")

    try:

        promotion = Promotion.objects.get(code=code)
        promotion.delete()
        messages.success(request, "successfully done")
    except Exception as e:
        messages.error(request, f"[ERROR]: {e}")
    return redirect(request, "moderate/promotion.html")
