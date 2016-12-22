from django import forms


class GuestCheckoutForm(forms.Form):
    email = forms.EmailField()
    email2 = forms.EmailField(label="Confirme o emai")

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')

        if email == email2:
            return email2
        else:
            forms.ValidationError("Endereço de email diferentes.")
