from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import AddressForm
from .models import UserAddress, UserCheckout


class AddressSelectFormView(FormView):
    form_class = AddressForm
    template_name = "orders/address_select.html"

    def get_form(self, *args, **kwargs):
        form = super(AddressSelectFormView, self).get_form(*args, **kwargs)
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
        form.fields['billing_address'].queryset = b_address
        form.fields['shipping_address'].queryset = s_address
        return form

    def form_valid(self, form, *args, **kwargs):
        billing_address = form.cleaned_data['billing_address']
        shipping_address = form.cleaned_data['shipping_address']
        self.request.session['billing_address_id'] = billing_address.id
        self.request.session['shipping_address_id'] = shipping_address.id
        return super(AddressSelectFormView, self).form_valid(form, *args, **kwargs)


    def get_success_url(self, *args, **kwargs):
        return '/checkout/'
