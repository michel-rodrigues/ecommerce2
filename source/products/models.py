from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify


class ProductQuerySet(models.query.QuerySet):

    def active(self):
        return self.filter(active=True)


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    # Altera o padrão de busca da query "all"
    def all(self, *args, **kwargs):
        return self.get_queryset().active()


class Product(models.Model):

    title = models.CharField(max_length=240)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    active = models.BooleanField(default=True)
    # slug
    # inventory

    # instanciando o objeto ProductManager, automaticamente a ListView só irá
    # retornar os objetos definidos no método 'all', sem precisar fazer
    # qualquer chamada na 'views.py'
    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'pk': self.pk})


class Variation(models.Model):
    product = models.ForeignKey(Product)
    title = models.CharField(max_length=120)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    sale_price = models.DecimalField(
            decimal_places=2,
            max_digits=20,
            null=True,
            blank=True
            )
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(null=True, blank=True) # refer none == unlimited amount

    def __str__(self):
        return self.title

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()


def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
    """
    Se o objeto MP3 Player for criado/alterado (salvo de alguma forma),
    os argumentos enviados serão:
    sender == <class 'products.models.Product'> # a classe
    instance == MP3 Player # a instancia da classe
    created == False # acho que indica se a instância acabou de ser criada
    """

    product = instance

    # Reverse Relation
    variations = product.variation_set.all() # É quase igual a instanciar
                                             # Variation.objects.filter(product=product)
    if variations.count() == 0:
        new_var = Variation()
        new_var.product = product
        new_var.title = "Default"
        new_var.price = product.price
        new_var.save()


post_save.connect(product_post_saved_receiver, sender=Product)


def image_upload_to(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    file_extension = filename(".")[1]
    # basename, file_extension = filename(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return "products/%s/%s" % (slug, new_filename)


class ProductImage(models.Model):

    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=image_upload_to)

    def __str__():
        return self.product.title
