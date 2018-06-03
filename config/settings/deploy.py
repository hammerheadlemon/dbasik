import os

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

INSTALLED_APPS.append('django_extensions')

ALLOWED_HOSTS = ['209.97.142.1']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'NAME': 'dbasik_dftgovernance',
        'USER': 'dbasik',
        'PORT': '5432',
        'PASSWORD': 'dbasik'
    }
}
