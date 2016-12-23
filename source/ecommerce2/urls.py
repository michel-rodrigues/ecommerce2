from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from .views import about
from carts.views import CartView, ItemCountView, CheckoutView
from orders.views import AddressSelectFormView, UserAddressCreateView


urlpatterns = [
    # Procura exatamente a palvara 'about', nessa sequência de letras
    url(r'^\babout\b', about, name='about'),
    url(r'^admin/', admin.site.urls),
    # url(r'^login/', login_view, name='login'),
    url(r'^', include('newsletter.urls', namespace='newsletter')),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^categories/',
        include('products.urls_categories', namespace='categories')
        ),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^cart/$', CartView.as_view(), name='cart'),
    url(r'^cart/count/$', ItemCountView.as_view(), name='item_count'),
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    url(r'^checkout/address/$',
        AddressSelectFormView.as_view(),
        name='order_address'
        ),
    url(r'^checkout/address/add/$',
        UserAddressCreateView.as_view(),
        name='user_address_crate'
        ),
]

if settings.DEBUG:
    urlpatterns += static(
            settings.STATIC_URL,
            document_root=settings.STATIC_ROOT
            )
    urlpatterns += static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT
            )
