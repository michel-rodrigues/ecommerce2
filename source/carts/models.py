from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save

from products.models import Variation


class  CartItem(models.Model):
    # o argumento é uma string pois a classe só será definida abaixo
    cart = models.ForeignKey('Cart')
    item = models.ForeignKey(Variation)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item.title

    def remove(self):
        return self.item.delete_from_cart()


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    # 'through' recebe o modelo intermediário
    items = models.ManyToManyField(Variation, through=CartItem)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.id)


def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = int(instance.quantity)
    if qty >= 1:
        price = instance.item.get_price()
        line_item_total = Decimal(qty) * Decimal(price)
        instance.line_item_total = line_item_total


pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)
