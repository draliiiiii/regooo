"""
Django settings for regois project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
import os
#import datetime
#from decouple import  Csv,config
from django.contrib.messages import constants as messages#new
#from six.moves import urllib


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nr9#8gpf1qo0j#wvno8%ru+d5h@95zcm)s4goshm82z=susd3e'


# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = config('DEBUG', default=False, cast=bool)

#ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())

FIXTURE_DIRS = (
   os.path.join(BASE_DIR, 'fixtures'),
)
# Build paths inside the project like this: BASE_DIR / 'subdir'.

#AUTH_USER_MODEL = 'authentication.AuthUser'

#AUTHENTICATION_BACKENDS = (
    #'django.contrib.auth.backends.ModelBackend',
    #'allauth.account.auth_backends.AuthenticationBackend',
#)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '70lui#+f1%64$8d4=h*s+&whyeb-n402%lrai_4oe%&dy$)^+7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*",]




IMPORT_EXPORT_USE_TRANSACTIONS = True

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
# new



INSTALLED_APPS = [
    'django_crontab',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #'templated_docs',
    'datetimewidget',

    #'rest_framework.authtoken',
    'django_listing',

    'daterange_filter',
    #'easy_select2',
    'bootstrap_datepicker_plus',


    'django.contrib.humanize',
    'django_extensions',
    'clinic',

    'django_tables2_reports',
    'crudbuilder',



    'rest_framework',
    'rest_framework.authtoken',

    'ckeditor',
    'ckeditor_uploader',
    'betterforms',
    #'django_filters',



    'django_tables2' ,
    'multiselectfield' ,
    'smart_selects' ,
    'djmoney',


    'django_select2',
    #'templatetags',

    'bootstrap4',
    'bootstrapform',

    #'widget_tweaks' ,
    'django_forms_bootstrap',
    'django_icons' ,

    'django_filters',
    'import_export',
    'thumb' ,
    'jsignature' ,
    'django_material_icons',

    'qr_code' ,
    #'authentication',
    'material',
    'bootstrap_modal_forms',
    'shapeshifter',


    'phonenumber_field',

    'mathfilters',

    'easy_thumbnails',
    'filer',
    'mptt',
    'django_pdf_overlay',
    'dal',
    'dal_select2',

    'dbbackup',

    'simple_select2',  # for bootstrap4 theme assets to be found
    'crispy_forms',
    'bulma',

    'debug_toolbar',
    'formsetfield',


    'wkhtmltopdf',



]
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': 'BASE_DIR/backups'}
CRONJOBS = [
('*/1 * * * *','regois.corn.my_backup')
]#'django.core.management.call_command', ['dbbackup'],{'-o':'2020-07/dbbackup_20200801.7z'}
#FILER_ENABLE_PERMISSIONS=True

#if you like run back up in  terminal run this code  python3 manage.py crontab add



CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_UPLOAD_PATH = "event-details/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}






CRISPY_TEMPLATE_PACK = 'bootstrap4'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',


    #'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.middleware.locale.LocaleMiddleware',



]

ROOT_URLCONF = 'regois.urls'

DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'django.core.context_processors.static',
                #'libraries':{
                    #'templatetag': 'aesthetics.templatetags.my_tags',

            ],
        },
    },

]






WSGI_APPLICATION = 'regois.wsgi.application'

#TINYMCE_DEFAULT_CONFIG = {
    #'plugins': "table,spellchecker,paste,searchreplace,image,imagetools,media,codesample,link,code",

    #'cleanup_on_startup': True,
    #'custom_undo_redo_levels': 10,


#}

#DIRECTORY = getattr(settings, "FILEBROWSER_DIRECTORY", 'uploads/')
#DIRECTORY = ''
#FILEBROWSER_DIRECTORY = 'filebrowser_uploads/'


#TINYMCE_SPELLCHECKER = True
#TINYMCE_COMPRESSOR = True

#TINYMCE_JS_ROOT = '/media/tiny_mce/'
#TINYMCE_JS_URL = "tiny_mce/tiny_mce_src.js"
#TINYMCE_DEFAULT_CONFIG = {
    #'plugins': "table,spellchecker,paste,searchreplace,image,imagetools,media,codesample,link,code",
    #'theme': "advanced",
#}

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_I18N = True

USE_L10N = True

USE_TZ = True


#Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
LOGIN_REDIRECT_URL="/authentication/dashboard/"
LOGOUT_REDIRECT_URL="/accounts/login/"





CURRENCY = 'SR'



REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}



MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


#STATICFILES_DIR =  [os.path.join(BASE_DIR,'customize_admin/static')]

# MEDIA Folder settings


#MEDIA_URL='/media/'
#MEDIA_ROOT=os.path.join(BASE_DIR,'media')
#STATIC_URL = '/static/'
#STATIC_ROOT=os.path.join(BASE_DIR,'static')


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



#STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files (Images)

# Crsipy forms
#CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Mapbox key define
#MAPBOX_KEY = "pk.eyJ1IjoibWlnaHR5c2hhcmt5IiwiYSI6ImNqd2duaW4wMzBhcWI0M3F1MTRvbHB0dWcifQ.1sDAD43q0ktK1Sr374xGfw"





#EMAIL_HOST="YOUR HOST"
#EMAIL_PORT=587
#EMAIL_HOST_USER='YOUR EMAIL'
#EMAIL_HOST_PASSWORD='YOUR PASWORD'
#EMAIL_USE_TLS=True

#ASGI_APPLICATION="simpleDjangoProject.routing.application"
#CHANNEL_LAYERS={
    #"default":{
        #"BACKEND":"channels.layers.InMemoryChannelLayer"
    #}
#}

#DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#INTERNAL_IPS = [
    #'127.0.0.1',
#]
#STRIPE_PUBLISHABLE_KEY = "***"
#STRIPE_SECRET_KEY = "****"
