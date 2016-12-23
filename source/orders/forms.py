from django import forms
from django.contrib.auth import get_user_model

from .models import UserAddress


User = get_user_model()


class GuestCheckoutForm(forms.Form):
    email = forms.EmailField()
    email2 = forms.EmailField(label="Confirme o email")

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email == email2:
            user_exists = User.objects.filter(email=email).count()
            if user_exists != 0:
                raise forms.ValidationError(
                        "Já existe um usuário com esse email."
                        )
            return email2
        else:
            raise forms.ValidationError("Endereço de email diferentes.")


class AddressForm(forms.Form):
    billing_address = forms.ModelChoiceField(
            queryset=UserAddress.objects.filter(address_type='billing'),
            empty_label=None,  # pode ser uma string também
            widget=forms.RadioSelect
            )
    shipping_address = forms.ModelChoiceField(
            queryset=UserAddress.objects.filter(address_type='shipping'),
            empty_label=None,
            # sem passar um widget é renderizado uma caixa de seleção com
            # dropdown
            widget=forms.RadioSelect
            )


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = (
            'address_type',
            'street',
            'city',
            'state',
            'zipcode',
            )
