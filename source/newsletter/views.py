from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail

from products.models import ProductFeatured, Product
from .forms import ContactForm, SignUpForm
from .models import SignUp


def home(request):

    # request.POST or None faz com que, ao carregar a página, não seja exibido
    # quais campos são obrigatórios. Do contrário, essas mensagens
    # seriam exibidas antes de qualquer ação do usuário
    form = SignUpForm(request.POST or None)

    products = Product.objects.all().order_by('?')[:6]
    featured_image = ProductFeatured.objects.first()

    context = {
        'title': "Sign Up Now",
        'form': form,
        'featured_image': featured_image,
        'products': products,
        }

    if form.is_valid():
        instance = form.save(commit=False)
        full_name = form.cleaned_data.get("full_name")
        if not full_name:
            full_name = "Your full name here"
        instance.full_name = full_name
        instance.save()
        context['title'] = 'Thank You'

    return render(request, "home.html", context)


def contact(request):

    title_align_center = False
    form = ContactForm(request.POST or None)

    if form.is_valid():

        form_email = form.cleaned_data.get('email')
        form_full_name = form.cleaned_data.get('full_name')
        form_message = form.cleaned_data.get('message')
        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'anotheremail@domain.com']
        contact_message = "%s: %s via %s" % (form_full_name, form_message, form_email)
        send_mail(subject, contact_message, from_email, to_email, fail_silently=True)

    context = {
        'form': form,
        'title': 'Contact Us',
        'title_align_center': title_align_center,
        }

    return render(request, "forms.html", context)
