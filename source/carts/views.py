from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from carts.models import Cart, CartItem
from products.models import Variation


class ItemCountView(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cart_id = self.request.session.get('cart_id')
            count = 0
            if cart_id:
                cart = Cart.objects.get(id=cart_id)
                count = cart.items.count()
            request.session["cart_item_count"] = count
            return JsonResponse({"count": count})
        else:
            Http404


class CartView(SingleObjectMixin, View):

    model = Cart
    template_name = 'carts/view.html'

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(3000)
        cart_id = self.request.session.get('cart_id')
        if cart_id == None:
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
                "total_items": total_items,
                "flash_message": flash_message
                }
            return JsonResponse(data)

        context = {
            'object': self.get_object(),
        }
        template = self.template_name
        return render(request, template, context)

