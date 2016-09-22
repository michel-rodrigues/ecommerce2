from django.views.generic.detail import DetailView
from django.shortcuts import render

from .models import Product


class ProductDetailView(DetailView):
    model = Product
