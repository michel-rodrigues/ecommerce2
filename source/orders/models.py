from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save

from carts.models import Cart


class UserCheckout(models.Model):
    user = models.OneToOneField(
            settings.AUTH_USER_MODEL,
            null=True,
            blank=True
            )
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


ADDRESS_TYPE = (
        ('billing', 'Cobrança'),
        ('shipping', 'Entrega')
        )


class UserAddress(models.Model):
    user = models.ForeignKey(UserCheckout)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPE)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return self.street

    def get_address(self):
        return "{}, {}, {} - {}".format(
                self.street,
                self.city,
                self.state,
                self.zipcode
                )


ORDER_STATUS_CHOICES = (
        ('created', 'Criado'),
        ('completed', 'Finalizado')
        )


class Order(models.Model):
    status = models.CharField(
            max_length=20,
            choices=ORDER_STATUS_CHOICES,
            default='created'
            )
    cart = models.ForeignKey(Cart)
    user = models.ForeignKey(UserCheckout, null=True)
    shipping_address = models.ForeignKey(
            UserAddress,
            related_name='shipping_address',
            null=True
            )
    billing_address = models.ForeignKey(
            UserAddress,
            related_name='billing_addressa',
            null=True
            )
    shipping_total_price = models.DecimalField(
            decimal_places=2,
            max_digits=10,
            default=5.99
            )
    order_total = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return str(self.cart.id)

    def mark_completed(self):
        self.status = 'completed'
        self.save()


def order_pre_save_receiver(sender, instance, *args, **kwargs):
    shipping_total_price = Decimal(instance.shipping_total_price)
    cart_total = Decimal(instance.cart.total)
    order_total = shipping_total_price + cart_total
    instance.order_total = order_total


pre_save.connect(order_pre_save_receiver, sender=Order)
