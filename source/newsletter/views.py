from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail

from .forms import ContactForm, SignUpForm
from .models import SignUp

def home(request):

    # Título que aparece em cima do formulário na página inicial.
    title = "Sign Up Now"

    # Apenas um teste pra exibir no terminal a requisição
    # if request.method == 'POST':
    #     print(request.POST)    

    # 'None' faz com que, ao carregar a página, não seja exibido
    # quais campos são obrigatórios. Do contrário, essas mensagens
    # seriam exibidas antes de qualquer ação do usuário
    form = SignUpForm(request.POST or None)

    context = {
        'title': title,
        'form': form,
    }

    # Verifica se está tudo correto nos campos do fomulário
    if form.is_valid():

        # 'form.save(commit=False)' permite receber os dados e
        # e alterá-los antes de serem enviados para o banco de dados.
        # Permite fazer alguma operação entre a ação do usuário de
        # enviar as informações e a ação de salvá-las no banco de dados
        instance = form.save(commit=False)

        # Testes de saída no terminal
        #print(instance.email)
        #print(instance.full_name)
        #print(instance.timestamp)

        # 'form.cleaned_data.get("full_name")' devolve uma string ao 
        # invés do objeto que possui essa string
        full_name = form.cleaned_data.get("full_name")

        # Se 'full_name' estiver vazio, receberá a string 
        # "Your full name here"
        if not full_name:
            full_name = "Your full name here"

        # o atributo 'full_name'(no caso o campo full name) recebe
        # a string armazanada na variável 'full_name'
        instance.full_name = full_name

        # salvando os dados do fomulário no banco de dados
        instance.save()

        context = {
            'title': 'Thank You',
        }

    # Passar contexto para o navbar.html se algum usuário 
    # está logado e se é parte da equipe( 'staff' é configurado na
    # página de admin, em 'Users')
    if request.user.is_authenticated() and request.user.is_staff:

        # Teste de saída no terminal
        # for instance in SignUp.objects.all():
        #     print(instance)
        #     print(instance.full_name)


        # ondernar pelo timestamp, o menos( - ) indica a 
        # ordem inversa do padrão
        #
        # o filter retorna somente as instancias cujo full_name
        # sejam 'Ana' ou 'ana' 
        # 
        # *não é case sensitive
        #
        #  ".filter(full_name__icontains=request.user)" retorna somente
        # as instancias cujo full_name sejam iguais ao usuário que fez 
        # a requisição
        #
        # também existe o __iexact
        #
        # queryset= SignUp.objects.all().order_by('-timestamp').filter(full_name__icontains="Ana")

        queryset = SignUp.objects.all().order_by('full_name')

        context = {
            "queryset": queryset,
        }


    elif request.user.is_authenticated():

        queryset = SignUp.objects.all().order_by('full_name')

        context = {
        "queryset": queryset,
        }


    return render(request, "home.html", context)


def contact(request):

    # 'title é chamado no template, na página 'contact.html'
    title = "Contact Us"

    # Essa variavel é chamada no template 
    title_align_center = False

    # 'None' faz com que, ao carregar a página, não seja exibido
    # quais campos são obrigatórios. Do contrário, essas mensagens
    # seriam exibidas antes de qualquer ação do usuário   
    form = ContactForm(request.POST or None)

    if form.is_valid():

        # ** Modos de capturar as informações do form **
        #
        #for key in form.cleaned_data:
        #    print(key)
        #    print(form.cleaned_data.get(key))

        #for key, value in form.cleaned_data.items():
        #    print(key, value) 

        # método 'cleaned_data.get' devolve uma string do objeto
        form_email = form.cleaned_data.get('email')
        form_full_name = form.cleaned_data.get('full_name')
        form_message = form.cleaned_data.get('message')
        #print(email, full_name, message)

        # Configura a mensagem e o para qual email será enviado
        # a mensagem da página contatos
        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'anotheremail@domain.com']
        contact_message = "%s: %s via %s" % (form_full_name, form_message, form_email)
        send_mail(subject, contact_message, from_email, to_email, fail_silently=True)

    context = {
        'form': form,
        'title': title,
        'title_align_center': title_align_center,
        }

    return render(request, "forms.html", context)
