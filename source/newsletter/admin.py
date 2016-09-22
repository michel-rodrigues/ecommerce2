from django.contrib import admin

from .forms import SignUpForm
from .models import SignUp

class SignUpAdmin(admin.ModelAdmin):
    # 'list display' e 'form' são viariáveis nativas do Django
    # para configurar o que será exibido na página admin
    # https://docs.djangoproject.com/en/1.9/ref/contrib/admin/

    list_display = ["__str__", "timestamp", "updated"]

    # SignUpForm possui uma classe 'Meta' 
    form = SignUpForm


    # 'class Meta' cria uma relação entre classes que permite
    # uma classe usar métodos de outra (pelo menos em outro
    # projeto foi o que pareceu ser)
    #
    # class Meta:
    #     model = SignUp

# Implementa a classe 'SignUp' declarada em 'models.py' 
# e a classe 'SignUpAdmin' dentro da página 'admin'
admin.site.register(SignUp, SignUpAdmin)
