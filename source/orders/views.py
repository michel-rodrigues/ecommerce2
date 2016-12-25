from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from .forms import AddressForm, UserAddressForm
from .mixins import CartOrderMixin, LoginRequiredMixin
from .models import UserAddress, UserCheckout, Order


class UserAddressCreateView(CreateView):
    form_class = UserAddressForm
    template_name = 'forms.html'
    success_url = '/checkout/address/'

    def get_checkout_user(self):
        user_check_id = self.request.session.get('user_checkout_id')
        user_checkout = UserCheckout.objects.get(id=user_check_id)
        return user_checkout

    def form_valid(self, form, *args, **kwargs):
        form.instance.user = self.get_checkout_user()
        return super(UserAddressCreateView, self).form_valid(form, *args, **kwargs)


class AddressSelectFormView(CartOrderMixin, FormView):
    form_class = AddressForm
    template_name = "orders/address_select.html"

    # .../ref/class-based-views/base/#django.views.generic.base.View.dispatch
    # https://ccbv.co.uk/projects/Django/1.10/django.views.generic.edit/FormView/
    def dispatch(self, *args, **kwargs):
        """
        Try to dispatch to the right method; if a method doesn't exist,
        defer to the error handler. Also defer to the error handler
        if the request method isn't on the approved list.
        """
        b_address, s_address = self.get_addresses()
        if b_address.count() == 0:
            messages.success(self.request, "Adicione um endereço para cobrança")
            return redirect('user_address_create')
        elif s_address.count() == 0:
            messages.success(self.request, "Adicione um endereço para entrega")
            return redirect('user_address_create')
        else:
            return super(AddressSelectFormView, self).dispatch(*args, **kwargs)

    def get_addresses(self, *args, **kwargs):
        user_check_id = self.request.session.get('user_checkout_id')
        user_checkout = UserCheckout.objects.get(id=user_check_id)
        b_address = UserAddress.objects.filter(
                user=user_checkout,
                address_type='billing'
                )
        s_address = UserAddress.objects.filter(
                user=user_checkout,
                address_type='shipping'
                )
        return b_address, s_address

    def get_form(self, *args, **kwargs):
        form = super(AddressSelectFormView, self).get_form(*args, **kwargs)
        b_address, s_address = self.get_addresses()
        form.fields['billing_address'].queryset = b_address
        form.fields['shipping_address'].queryset = s_address
        return form

    def form_valid(self, form, *args, **kwargs):
        billing_address = form.cleaned_data['billing_address']
        shipping_address = form.cleaned_data['shipping_address']
        order = self.get_order()
        order.billing_address = billing_address
        order.shipping_address = shipping_address
        order.save()
        # self.request.session['billing_address_id'] = billing_address.id
        # self.request.session['shipping_address_id'] = shipping_address.id
        return super(AddressSelectFormView, self).form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return '/checkout/'


class OrderList(LoginRequiredMixin, ListView):

    template_name = 'orders/orders_list.html'

    def get_queryset(self):
        # user_check_id = self.request.user.id
        user_checkout_email = self.request.user.email
        try:
            user_checkout = UserCheckout.objects.get(email=user_checkout_email)
        except UserCheckout.DoesNotExist:
            user_checkout = None
        queryset = Order.objects.filter(user=user_checkout.id)
        return queryset


class OrderDetail(DetailView):
    model = Order

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            user_checkout_email = self.request.user.email
            user_checkout = UserCheckout.objects.get(email=user_checkout_email)
        else:
            try:
                user_checkout_id = self.request.session.get('user_checkout_id')
                user_checkout = UserCheckout.objects.get(id=user_checkout_id)
            except UserCheckout.DoesNotExist:
                user_checkout = UserCheckout.objects.get(user=request.user)
            except:
                user_checkout = None
        obj = self.get_object()  # método herdado do DetailView
        if obj.user == user_checkout and user_checkout is not None:
            return super(OrderDetail, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404
