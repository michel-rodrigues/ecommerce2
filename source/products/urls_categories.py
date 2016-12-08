from django.conf.urls import url

from .views import CategoryDetailView, CategoryListView

urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name='category_list'),
    url(r'^(?P<slug>[\w-]+)/$', CategoryDetailView.as_view(), name='category_detail'),
]
