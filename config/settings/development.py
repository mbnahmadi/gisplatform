import os
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gis_dev',
        'USER': 'postgres',
        'PASSWORD': '123456789',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' خروجی ایمیل در کنسول




