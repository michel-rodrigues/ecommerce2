from django.core.urlresolvers import reverse
from django.db import models


class Product(models.Model):

    title = models.CharField(max_length=240)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    active = models.BooleanField(default=True)
    # slug
    # inventory

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'pk': self.pk})
