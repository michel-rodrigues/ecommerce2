from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render
# from django.utils import timezone

from .models import Product


class ProductDetailView(DetailView):
    model = Product

    # Definição implícita da localização do template
    # template_name = "<appname>/<modelname>_detail.html"


class ProductListView(ListView):
    model = Product
    # Passa um filtro diferente do padrão
    # queryset = Product.objects.filter(active=False)

    # Se o método 'all' for instanciado, então é utilizado o método 
    # padrão retornando todos os objetos do BD
    # queryset = Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)

        '''
        context['now'] = timezone.now()

        print(context)

        {'product_list': <QuerySet [<Product: Smartphone AX5>, <Product: MP3
        Player>, <Product: DVD - O Poderoso Chefão>]>, 'page_obj': None,
        'object_list': <QuerySet [<Product: Smartphone AX5>, <Product: MP3
        Player>, <Product: DVD - O Poderoso Chefão>]>, 'is_paginated':
        False, 'paginator': None, 'view': <products.views.ProductListView
        object at 0xb5b7fd6c>}
        '''
        return context
