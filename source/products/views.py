from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
# from django.utils import timezone

from .forms import VariationInventoryFormSet
from .mixins import LoginRequiredMixin, StaffRequiredMixin
from .models import Product, Variation


class ProductDetailView(DetailView):
    model = Product

    # Definição implícita da localização do template
    # template_name = "<appname>/<modelname>_detail.html"


class ProductListView(ListView):
    model = Product
    # Passa um filtro diferente do padrão
    # queryset = Product.objects.filter(active=False)

    # Se o método 'all' for instanciado aqui (ver models.py), então é utilizado o método 
    # padrão retornando todos os objetos do BD
    queryset = Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')

        # Força a declaração '/?q=', se não houver levanta uma exceção
        # context['query'] = self.request.GET['q']
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

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = self.model.objects.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(price__icontains=query)
                )
            # try:
            #     qs_price = self.models.objects.filter(
            #             Q(price=query)
            #         )
            #     qs = (qs | qs_price).distinct()
            # except:
            #     print("DEU RUIM!!!")
        return qs


class VariationListView(StaffRequiredMixin, ListView):
    model = Variation
    queryset = Variation.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(VariationListView, self).get_context_data(*args, **kwargs)
        context['formset'] = VariationInventoryFormSet(queryset=self.get_queryset())
        return context

    def get_queryset(self, *args, **kwargs):
        product_pk = self.kwargs.get('pk')
        if product_pk:
            product = get_object_or_404(Product, pk=product_pk)
            queryset = Variation.objects.filter(product=product)
        return queryset

    def post(self, request, *args, **kwargs):
        # request.POST
        formset = VariationInventoryFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                if new_item.title:
                    product_pk = self.kwargs.get('pk')
                    product = get_object_or_404(Product, pk=product_pk)
                    new_item.product = product
                    new_item.save()
                    form.save()
            messages.success(request, 'Inventário e preços atualizados.')
            return redirect('products:list')
        raise Http404
