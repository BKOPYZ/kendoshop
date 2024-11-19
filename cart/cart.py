from statistics import quantiles
from django.conf import settings

from core.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def load_from_database(self, request):
        pass

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
            self.cart[product_id] -= quantity

        if self.cart[product_id] <= 0:
            return self.delete(product), 0

        self.session.modified = True
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
