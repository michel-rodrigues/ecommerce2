from django.contrib import admin

from .models import Product, Variation, ProductImage, Category

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Variation)
admin.site.register(Category)
