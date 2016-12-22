from django import forms
from django.contrib.auth import get_user_model


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
    billing_address = forms.CharField()
    shipping_address = forms.CharField()
