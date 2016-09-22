from django import forms
#import re

from .models import SignUp

# Esse fomulário é o da página contato
# 'required=False' indica que o campo não é obrigatório
class ContactForm(forms.Form):
    full_name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class SignUpForm(forms.ModelForm):
    # a sub-classe Meta faz com que essa classe receba os atributos
    # da classe SignUp em models.py
    # os campos 'full_name' e 'email' foram declarados na classe SignUp
    class Meta:
        model = SignUp
        fields = ['full_name', 'email']

    # Esse método limita o tipo de domínio aceito para o registro
    def clean_email(self):

        # 'self.cleaned_data.get(email)' devolve uma string ao invés do 
        # objeto que possui essa string
        email = self.cleaned_data.get('email')

        # só captura com um ponto
        #
        # email_base, email_provider = email.split('@')
        # domain, extension = email_provider.split('.')

        # captura tudo o que está entre @ e o primeiro ponto (.) e 
        # devolve uma lista (dev: jpnogueira)
        # 
        # domain = re.findall(r'@([\w]+[^\.])', email)
        # domain = domain[0]

        # método 'find' da classe 'string', vai devolver o que estiver
        # entre o caracter '@' e o primeiro '.'(ponto) que encontrar 
        domain = email[email.find("@")+1:email.find(".")]

        # Se a string em 'domain' não for 'debian' levanta uma exceção e
        # exibe uma mensagem ná pagina pro usuário
        if not domain == "debian":
            raise forms.ValidationError("Please use a valid distro email adress")
        return email
