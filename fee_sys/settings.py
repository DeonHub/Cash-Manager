"""
Django settings for fee_sys project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
import environ

env = environ.Env()
environ.Env.read_env()


# import django_heroku 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static/js', 'serviceworker.js')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# print(os.environ.get('SECRET_KEY'))
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# AUTH_USER_MODEL = 'superuser.User' 

# Application definition

INSTALLED_APPS = [
    'superuser',
    'client',
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
    'django_filters',
    'cloudinary_storage',
    'cloudinary',
    'login',
    'api',
    # 'main',
    'rest_framework',
    'drf_yasg',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'fee_sys.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'superuser.context_processors.counter',
                # 'superuser.context_processors.checkSession',
                

                # 'login.context_processors.getClientDetails',

            ],
        },
    },
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

WSGI_APPLICATION = 'fee_sys.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

IN_PRODUCTION_MODE = env("IN_PRODUCTION_MODE")

if IN_PRODUCTION_MODE:
    BASE_URL = 'http://127.0.0.1:8000/'
else:
    BASE_URL = 'https://cash.akwaabasoftware.com/'


STATIC_URL = 'static/'

STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/' 

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DATETIME_FORMAT': '%d %B, %Y'
}


CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUD_NAME'),
    'API_KEY': env('API_KEY'),
    'API_SECRET': env('API_SECRET')
}


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# Default primary key field typ
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = '1025'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = False
# # EMAIL_USE_SSL = False
# EMAIL_HOST_USER=impraimgideon89@gmail.com
# EMAIL_HOST_PASSWORD=erhbudvffukfvlyh

EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')





# PWA_APP_NAME = 'fee_sys'
# PWA_APP_DESCRIPTION = "FMS PWA"
# PWA_APP_THEME_COLOR = '#000000'
# PWA_APP_BACKGROUND_COLOR = '#ffffff'
# PWA_APP_DISPLAY = 'standalone'
# PWA_APP_SCOPE = '/'
# PWA_APP_ORIENTATION = 'any'
# PWA_APP_START_URL = '/'
# PWA_APP_STATUS_BAR_COLOR = 'default'
# PWA_APP_ICONS = [
# 	{
# 		'src': 'static/superuser/media/favicon.jpg',
# 		'sizes': '125x125'
# 	}
# ]

# PWA_APP_ICONS_APPLE = [
# 	{
# 		'src': 'static/superuser/media/favicon.jpg',
# 		'sizes': '125x125'
# 	}
# ]



# PWA_APP_DIR = 'ltr'
# PWA_APP_LANG = 'en-US'


SWAGGER_SETTINGS = {

    'VALIDATOR_URL': 'http://localhost:8000',

}
# DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S' 
# DATETIME_FORMAT = '%d-%m-%Y' 
# USE_L10N = False
# USE_TZ = False