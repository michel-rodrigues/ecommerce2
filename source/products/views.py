from django.views.generic.detail import DetailView
from django.shortcuts import render

from .models import Product


class ProductDetailView(DetailView):
    model = Product

    # Definição implícita da localização do template
    # template_name = "<appname>/<modelname>_detail.html"
