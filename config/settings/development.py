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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # یا سرور ایمیل خودت
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'pmetoceans@gmail.com'
EMAIL_HOST_PASSWORD = 'cvsz lvlj vtut brgx'


