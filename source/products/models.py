from django.core.urlresolvers import reverse
from django.db import models


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
