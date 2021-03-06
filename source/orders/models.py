from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save

from decimal import Decimal
import braintree

from carts.models import Cart


if settings.DEBUG:
    braintree.Configuration.configure(
                braintree.Environment.Sandbox,
                merchant_id=settings.BRAINTREE_MERCHANT_ID,
                public_key=settings.BRAINTREE_PUBLIC,
                private_key=settings.BRAINTREE_PRIVATE
                )


class UserCheckout(models.Model):
    user = models.OneToOneField(
            settings.AUTH_USER_MODEL,
            null=True,
            blank=True
            )
    email = models.EmailField(unique=True)
    braintree_id = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.email

    @property
    def get_braintree_id(self):
        if not self.braintree_id:
            result = braintree.Customer.create({
                        'email': self.email,
                        })
            if result.is_success:
                self.braintree_id = result.customer.id
                self.save()
        return self.braintree_id

    def get_client_token(self):
        customer_id = self.get_braintree_id
        if customer_id:
            client_token = braintree.ClientToken.generate({
                    # caso exista, recupera as informações do cliente
                    # se essa linha for retirada, a cada transação será pedido
                    # ao cliente para inserir suas informações de cobrança
                    "customer_id": customer_id
                    })
            return client_token
        return None


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
        ('paid', 'Pago'),
        ('shipped', 'Finalizado')
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
    order_id = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.cart.id)

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})

    def mark_completed(self, order_id=None):
        if order_id and not self.order_id:
            self.order_id = order_id
        self.status = 'paid'
        self.save()


def update_braintree_id_receiver(sender, instance, *args, **kwargs):
    if not instance.braintree_id:
        instance.get_braintree_id


def order_pre_save_receiver(sender, instance, *args, **kwargs):
    shipping_total_price = Decimal(instance.shipping_total_price)
    cart_total = Decimal(instance.cart.total)
    order_total = shipping_total_price + cart_total
    instance.order_total = order_total


post_save.connect(update_braintree_id_receiver, sender=UserCheckout)

pre_save.connect(order_pre_save_receiver, sender=Order)
