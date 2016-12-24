from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, FormView

from .forms import AddressForm, UserAddressForm
from .mixins import CartOrderMixin
from .models import UserAddress, UserCheckout


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
            return redirect('user_address_crate')
        elif s_address.count() == 0:
            messages.success(self.request, "Adicione um endereço para entrega")
            return redirect('user_address_crate')
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
