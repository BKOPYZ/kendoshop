from urllib import request
from django.conf import settings
from cart.models import ShoppingSession, CartItem
from userauths.models import User

from core.models import Product
from copy import deepcopy


class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def load_from_database(self, request):
        old_cart = deepcopy(self.cart)
        if request.user.is_authenticated:
            try:
                user = User.objects.get(user_id=request.user.user_id)
                cart = ShoppingSession.objects.get(user=user)
                cartItems = CartItem.objects.filters(user=user)
                for cartItem in cartItems:
                    self.cart[cartItem.product.product_id] = cartItem.quantity

            except ShoppingSession.DoesNotExist:
                cart = ShoppingSession.objects.create(user=user)
                cart.save()

        if old_cart:
            for product_id, quantity in self.cart.itmes():
                product = Product.objects.get(product_id=product_id)

                cartItem = CartItem.objects.create(
                    cart=cart, product=product, quantity=quantity
                )
                cartItem.save()
        self.session.modified = True

    def add(self, product, quantity):
        # add to table
        product_id = str(product.product_id)
        product_qty = str(quantity)
        status = 0
        if product_id in self.cart:
            self.cart[product_id] += int(product_qty)

        else:
            self.cart[product_id] = int(product_qty)

        if product.quantity < self.cart[product_id]:
            status = 1
            self.cart[product_id] -= int(quantity)

        if self.cart[product_id] <= 0:
            return self.delete(product), 0

        self.session.modified = True
        # TODO: add to database
        return status, self.cart[product_id]

    def delete(self, product):
        product_id = str(product.product_id)
        self.cart.pop(product_id)
        self.session.modified = True
        return 2

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        product_ids = self.cart.keys()
        quantities = self.cart.values()

        print("---------------")
        print(product_ids)
        print(quantities)
        print("---------------")

        products = Product.objects.filter(product_id__in=product_ids)

        return [(product, self.cart[str(product.product_id)]) for product in products]
