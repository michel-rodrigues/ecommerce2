from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormMixin

import braintree

from .models import Cart, CartItem
from orders.forms import GuestCheckoutForm
from orders.mixins import CartOrderMixin
from orders.models import UserCheckout, Order
from products.models import Variation


class ItemCountView(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cart_id = self.request.session.get("cart_id")
            count = 0
            if cart_id:
                cart = Cart.objects.get(id=cart_id)
                count = cart.items.count()
            request.session["cart_item_count"] = count
            return JsonResponse({"count": count})
        else:
            raise Http404


class CartView(SingleObjectMixin, View):

    model = Cart
    template_name = 'carts/view.html'

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(3000)
        cart_id = self.request.session.get('cart_id')
        if cart_id is None:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()
        return cart

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        item_id = request.GET.get('item')
        delete_item = request.GET.get('delete', False)
        item_added = False
        flash_message = ''

        if item_id:
            item_instance = get_object_or_404(Variation, id=item_id)
            qty = request.GET.get('qty', 1)
            try:
                if int(qty) < 1:
                    delete_item = True
            except:
                raise Http404
            cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    item=item_instance
                    )
            if created:
                item_added = True
                flash_message = "Produto adicionado ao carrinho de compras"
            if delete_item:
                cart_item.delete()
                flash_message = "Produto removido do carrinho de compras"
            else:
                cart_item.quantity = qty
                cart_item.save()
                flash_message = "Quantidade do produto atualizada"
            if not request.is_ajax():
                return HttpResponseRedirect(reverse('cart'))

        if request.is_ajax():
            try:
                total = cart_item.line_item_total
            except:
                total = None

            try:
                cart_total = cart_item.cart.total
            except:
                cart_total = None

            try:
                tax_total = cart_item.cart.tax_total
            except:
                tax_total = None

            try:
                subtotal = cart_item.cart.subtotal
            except:
                subtotal = None

            try:
                total_items = cart_item.cart.items.count()
            except:
                total_items = 0

            data = {
                "deleted": delete_item,
                "item_added": item_added,
                "line_total": total,
                "subtotal": subtotal,
                "cart_total": cart_total,
                "tax_total": tax_total,
                "total_items": total_items,
                "flash_message": flash_message
                }
            return JsonResponse(data)

        context = {
            'object': self.get_object(),
        }
        template = self.template_name
        return render(request, template, context)


class CheckoutView(CartOrderMixin, FormMixin, DetailView):

    # https://docs.djangoproject.com/en/1.10/ref/class-based-views/mixins-editing/#formmixin
    # https://ccbv.co.uk/projects/Django/1.10/django.views.generic.edit/FormMixin/

    model = Cart
    template_name = 'carts/checkout_view.html'
    form_class = GuestCheckoutForm  # herdado de FormMixin

    # ############################################################
    # tudo está comentado porque orders.mixins.CartOrderMixin está
    # executando a função desse código
    # ############################################################

    # def get_object(self, *args, **kwargs):
    #     cart_id = self.request.session.get('cart_id')
    #     if cart_id is None:
    #         return redirect('cart')
    #     cart = Cart.objects.get(id=cart_id)
    #     return cart

    # def get_order(self, *args, **kwargs):
    #     cart = self.get_object()
    #     new_order_id = self.request.session.get('order_id')
    #     if new_order_id is None:
    #         new_order = Order.objects.create(cart=cart)
    #         self.request.session['order_id'] = new_order.id
    #     else:
    #         new_order = Order.objects.get(id=new_order_id)
    #     return new_order

    # método foi implemetado após a crição de orders.mixins.CartOrderMixin
    def get_object(self, *args, **kwargs):
        cart = self.get_cart()
        # me pareceram desnecessárias essas duas linhas
        # if cart is None:
        #     return None
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)
        user_can_continue = False
        user_check_id = self.request.session.get('user_checkout_id')
        if not self.request.user.is_authenticated() and user_check_id is None:
            context['login_form'] = AuthenticationForm()
            # .../ref/request-response/#django.http.HttpRequest.build_absolute_uri
            context['next_url'] = self.request.build_absolute_uri()
        elif self.request.user.is_authenticated():
            user_checkout, _ = UserCheckout.objects.get_or_create(
                    email=self.request.user.email
                    )
            user_checkout.user = self.request.user
            self.request.session['user_checkout_id'] = user_checkout.id
            context['client_token'] = user_checkout.get_client_token()
            user_can_continue = True
        elif user_check_id is not None:
            user_checkout = UserCheckout.objects.get(id=user_check_id)
            context['client_token'] = user_checkout.get_client_token()
            user_can_continue = True
        else:
            pass
        context['order'] = self.get_order()
        context['user_can_continue'] = user_can_continue
        context['form'] = self.get_form()  # Herdado de FormMixin
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user_checkout, _ = UserCheckout.objects.get_or_create(email=email)
            request.session['user_checkout_id'] = user_checkout.id
            self.request.session['user_checkout_id'] = user_checkout.id
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # Herdado de FormMixin
    def get_success_url(self):
        return reverse('checkout')

    def get(self, request, *args, **kwargs):
        get_data = super(CheckoutView, self).get(request, *args, **kwargs)
        cart = self.get_object()
        if cart is None:
            return redirect('cart')
        new_order = self.get_order()
        user_checkout_id = request.session.get('user_checkout_id')

        if user_checkout_id is not None:
            user_checkout = UserCheckout.objects.get(id=user_checkout_id)

            # adicionado depois de criar orders.mixins.CartOrderMixin
            # não fazia parte desse bloco 'if'
            if new_order.billing_address is None or new_order.shipping_address is None:
                return redirect('order_address')

            # ############################################################
            # tudo está comentado porque orders.mixins.CartOrderMixin está
            # executando a função desse código
            # ############################################################
            #
            # billing_address_id = request.session.get('billing_address_id')
            # shipping_address_id = request.session.get('shipping_address_id')

            # if billing_address_id is None or shipping_address_id is None:
            #     return redirect('order_address')
            # else:
            #     billing_address = UserAddress.objects.get(id=billing_address_id)
            #     shipping_address = UserAddress.objects.get(id=shipping_address_id)

            new_order.user = user_checkout
            # new_order.billing_address = billing_address
            # new_order.shipping_address = shipping_address
            new_order.save()

        return get_data


class CheckoutFinalView(CartOrderMixin, View):

    def post(self, request, *args, **kwargs):
        order = self.get_order()
        order_total = order.order_total
        nonce = request.POST.get("payment_method_nonce")
        if nonce:
            result = braintree.Transaction.sale({
                "amount": order_total,
                "payment_method_nonce": nonce,
                "billing": {
                    "postal_code": "{}".format(order.billing_address.zipcode),
                    "street_address": "{}".format(order.billing_address.street),
                    "locality": "{}".format(order.billing_address.city),
                    "region": "{}".format(order.billing_address.state)
                    },
                "options": {
                    "submit_for_settlement": True
                    }
                })
        if result.is_success:
            # print(result.transaction.id)
            # print(result.transaction.type)
            # print(result.transaction.status)
            order_id = result.transaction.id
            order.mark_completed(order_id=order_id)
            messages.success(request, 'Compra finalizada.')
            del request.session['cart_id']
            del request.session['order_id']
        else:
            messages.success(request, '{}'.format(result.message))
            return redirect('checkout')
        return redirect('order_detail', pk=order.pk)

    def get(self, request, *args, **kwargs):
         return redirect('checkout')
