from django.conf.urls import url

from .views import (
            ProductDetailView,
            ProductListView,
        )

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='detail'),
    url(r'^$', ProductListView.as_view(), name='list'),
]

