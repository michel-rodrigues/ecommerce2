from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.shortcuts import render, get_object_or_404

from carts.models import Cart, CartItem
from products.models import Variation


class CartView(View):

    def get(self, request, *args, **kwargs):
        item_id = request.GET.get('item')
        delete_item = request.GET.get('delete')
        if item_id:
            item_instance = get_object_or_404(Variation, id=item_id)
            qty = request.GET.get('qty')
            cart = Cart.objects.first()
            cart_item = CartItem.objects.get_or_create(
                    cart=cart,
                    item=item_instance
                    )[0]
            if delete_item:
                cart_item.delete()
            else:
                cart_item.quantity = qty
                cart_item.save()
        return HttpResponseRedirect('/')

