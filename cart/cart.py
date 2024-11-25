from itertools import product
from urllib import request
from django.conf import settings
from django.shortcuts import get_object_or_404
import cart
from cart.models import ShoppingSession, CartItem
from userauths.models import User

from core.models import Product, Promotion
from copy import deepcopy
from django import template

register = template.Library()

class Cart:

    def __init__(self, request):
        self.request = request
        self.session = request.session

        promotion = self.session.get(settings.PROMOTION_SESSION_ID)
        if not promotion:
            # save an empty cart in the session
            promotion = self.session[settings.PROMOTION_SESSION_ID] = {}
        self.promotion = promotion

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
            self.load_from_database(cart)

        # payment = self.session.get(settings.PAYMENT_SESSION_ID)
        # if not payment:
        #     # save an empty cart in the session
        #     payment = self.session[settings.PAYMENT_SESSION_ID] = {}

        # self.payment = payment
        self.cart = cart

    def load_from_database(self, cart: dict = dict()):
        if not hasattr(self, "cart"):
            self.cart = cart
        old_cart = deepcopy(self.cart)
        if self.request.user.is_authenticated:
            try:

                self.cartObject = ShoppingSession.objects.get(user=self.request.user)
                cartItems = CartItem.objects.filter(cart=self.cartObject)
                for cartItem in cartItems:
                    self.cart[cartItem.product.product_id] = cartItem.quantity
                if self.cartObject.promotion:
                    self.promotion.update(self.cartObject.promotion.to_dict())
            except ShoppingSession.DoesNotExist:
                self.cartObject = ShoppingSession.objects.create(user=self.request.user)
                self.cartObject.save()

            if hasattr(self, "cart") and old_cart:
                for product_id, quantity in old_cart.items():
                    product = Product.objects.get(product_id=product_id)
                    try:
                        cartItem = CartItem.objects.get(
                            cart=self.cartObject, product=product
                        )
                    except CartItem.DoesNotExist:
                        cartItem = CartItem.objects.create(
                            cart=self.cartObject, product=product, quantity=quantity
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
        if self.request.user.is_authenticated:
            try:
                self.cartObject = ShoppingSession.objects.get(user=self.request.user)
                cart_item = CartItem.objects.get(product=product, cart=self.cartObject)
                cart_item.quantity = self.cart[product_id]
                cart_item.save()

            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(
                    product=product,
                    cart=self.cartObject,
                    quantity=self.cart[product_id],
                )
                cart_item.save()

        return status, self.cart[product_id]

    def delete(self, product):
        product_id = str(product.product_id)
        self.cart.pop(product_id)
        self.session.modified = True

        if self.request.user.is_authenticated:
            self.cartObject = ShoppingSession.objects.get(user=self.request.user)
            cart_item = CartItem.objects.get(product=product, cart=self.cartObject)
            cart_item.delete()
        return 2

    def use_promotion(self, code: str):
        try:
            promotion = Promotion.objects.get(code=code)
            if promotion.amount <= 0:
                return False
        except Promotion.DoesNotExist:
            return False

        self.promotion.update(promotion.to_dict())
        self.session.modified = True

        if self.request.user.is_authenticated:
            shopping_cart = ShoppingSession.objects.get(user=self.request.user)
            shopping_cart.promotion = promotion
            shopping_cart.save()

        return True

    def unused_promotion(self):
        self.promotion.clear()
        self.session.modified = True
        cart_object = ShoppingSession.objects.get(user=self.request.user)
        cart_object.promotion = None
        cart_object.save()

    def delete_cart(self):
        self.cart.clear()
        self.promotion.clear()
        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        product_ids = self.cart.keys()
        quantities = self.cart.values()

        products = Product.objects.filter(product_id__in=product_ids)

        return [(product, self.cart[str(product.product_id)]) for product in products]

    @property
    def calculate_total_price(self):
        total_price = self.get_total_price
        discount = self.get_discount
        return total_price - discount

    @property
    def get_total_price(self):
        total_price = 0
        for product_id, quantity in self.cart.items():
            product = get_object_or_404(Product, product_id=product_id)
            total_price += product.price * quantity
        return float(total_price)

    @property
    def get_discount(self):
        if self.promotion.get("code") is None:
            return 0
        return float(self.get_total_price) * float(self.promotion.get("discount"))

    @property
    def get_discount_frac(self):
        if self.promotion.get("code") is None:
            return 0
        return float(self.promotion.get("discount"))
