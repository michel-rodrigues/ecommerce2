from django.apps import AppConfig

"""

Esse arquivo é criado para ajudar o usuário a incluir qualquer configuração da aplicação no projeto.
Usando isso você pode configurar algum atributo da aplicação.

Da documentação 'Configuração de Aplicação':

Objetos de configuração de aplicação armazenam metadados para uma aplicação. Alguns atributos podem
ser configurados na subclasse AppConfig. Outras são configurados pelo django e apenas lidos.

Exemplo da documentação:

Digamos que você está criando uma 'pluggable app' chamada "Rock 'n' roll", então fornece um
nome apropriado, como a seguir.

Dentro da aplicação rock_n_roll, nós criamos a classe RockNRollConfig que herda da classe AppConfig.

#rock_n_roll/apps.py
from django.apps import AppConfig

class RockNRollConfig(AppConfig): # Our app config class
    name = 'rock_n_roll'
    verbose_name = "Rock ’n’ roll"

Nós podemos fazer sua aplicação carregar, por padrão, esta subclasse de AppConfig especificando
a variável 'default_app_config' dentro do arquivo 'rock_n_roll/__init__.py'.

# rock_n_roll/__init__.py
default_app_config = 'rock_n_roll.apps.RockNRollConfig'

Com isso, RockNRollConfig será chaamado mesmo que INSTALLED_APPS apenas contenha 'rock_n_roll'.
Isso nos permite fazer com que os atributos de AppConfig sejam chamdos sem a necessidade do
usuário atualizar as configurações de INSTALLED_APPS.

Fonte: http://stackoverflow.com/questions/32795227/what-is-the-purpose-of-apps-py-in-django-1-9

"""

class NewsletterConfig(AppConfig):
    name = 'newsletter'
