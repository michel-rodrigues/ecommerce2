from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from carts.models import Cart
from .models import Order


class LoginRequiredMixin:

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class CartOrderMixin:

    def get_cart(self):
        cart_id = self.request.session.get('cart_id')
        if cart_id is None:
            return None
        cart = Cart.objects.get(id=cart_id)
        if cart.items.count() <= 0:
            return None
        return cart

    def get_order(self):
        cart = self.get_cart()
        if cart is None:
            return None
        new_order_id = self.request.session.get('order_id')
        if new_order_id is None:
            new_order = Order.objects.create(cart=cart)
            self.request.session['order_id'] = new_order.id
        else:
            new_order = Order.objects.get(id=new_order_id)
        return new_order
