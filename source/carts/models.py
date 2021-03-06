from decimal import Decimal, ROUND_DOWN
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete

from products.models import Variation


class CartItem(models.Model):
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
    subtotal = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    tax_percentage = models.DecimalField(max_digits=4, decimal_places=3, default=0.085)
    tax_total = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.id)

    def update_subtotal(self):
        subtotal = 0
        items = self.cartitem_set.all()
        for item in items:
            subtotal += item.line_item_total
        self.subtotal = subtotal
        self.save()


def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = int(instance.quantity)
    if qty >= 1:
        price = instance.item.get_price()
        line_item_total = Decimal(qty) * Decimal(price)
        instance.line_item_total = line_item_total


def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_subtotal()


def do_tax_and_total_receiver(sender, instance, *args, **kwargs):

    subtotal = Decimal(instance.subtotal)
    tax_percentage = Decimal(instance.tax_percentage)

    tax_total = subtotal * tax_percentage
    total = subtotal + tax_total

    tax_total = tax_total.quantize(Decimal('.01'), rounding=ROUND_DOWN)
    total = total.quantize(Decimal('.01'), rounding=ROUND_DOWN)

    instance.tax_total = tax_total
    instance.total = total


pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)

post_save.connect(cart_item_post_save_receiver, sender=CartItem)

post_delete.connect(cart_item_post_save_receiver, sender=CartItem)

pre_save.connect(do_tax_and_total_receiver, sender=Cart)
