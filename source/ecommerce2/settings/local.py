"""
Django settings for e-Commerce 2 project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&6hz!f!%fa^8$4d&=2-onjt5w!ixkr=p=##oki2lxb6*576#dg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Definições para email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_password'
EMAIL_PORT = 587
EMAIL_USE_TSL = True

'''
If using gmail, you will need to
unlock Captcha to enable Django
to send for you:
https://accounst.google/displayunlockcaptcha
'''

# Application definition

INSTALLED_APPS = [
    #django app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #third party apps
    'crispy_forms',
    'registration',
    #my apps
    'newsletter',
    'products',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce2.urls'

# Por padrão o django procura os templates dentro de uma pasta 'templates'
# no diretório do aplicativo  
# 'DIRS': [os.path.join(BASE_DIR, "templates")], configura o django
# para procurar a pasta 'templates' no diretório raiz do projeto
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"), ""],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "public/static")

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "public/media")

#Crispy Form Tags SETTINGS
CRISPY_TEMPLATE_PACK = 'bootstrap3'


#Djando Registration Redux SETTINGS
ACCOUNT_ACTIVATION_DAYS = 7
"""This is the number of days users will have to activate their accounts after registering. If a user does not activate within that period, the account will remain permanently inactive and may be deleted by maintenance scripts provided in django-registration-redux."""

REGISTRATION_AUTO_LOGIN = True
"""Optional. If this is True, your users will automatically log in when they click on the activation link in their email. Defaults to False."""

#REGISTRATION_DEFAULT_FROM_EMAIL
"""Optional. If set, emails sent through the registration app will use this string. Falls back to using Django’s built-in DEFAULT_FROM_EMAIL setting."""

#REGISTRATION_EMAIL_HTML
"""Optional. If this is False, registration emails will be send in plain text. If this is True, emails will be sent as HTML. Defaults to True."""

#NÃO ENTENDI, MAS FEZ FUNCIONA A TELA DE LOGIN 
SITE_ID = 1

#Redireciona após o login
LOGIN_REDIRECT_URL = "/"
