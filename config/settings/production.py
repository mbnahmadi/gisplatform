from .base import *

DEBUG = False
ALLOWED_HOSTS = ['gisplatform.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gis_prod',
        'USER': 'gisuser',
        'PASSWORD': os.getenv("PROD_DB_PASS"),
        'HOST': 'prod-db-server',  # برای داکر همچین چیزی نوشته شده
        'PORT': '5432',
    }
}


#این‌ها فقط باید در production روشن باشن.
SECURE_SSL_REDIRECT = True   #اجبار به استفاده از HTTPS
SESSION_COOKIE_SECURE = True  #حفاظت از کوکی سشن در HTTPS 
CSRF_COOKIE_SECURE = True   #حفاظت از کوکی CSRF در HTTPS   #اگر این True باشه، CSRF Token فقط از طریق HTTPS فرستاده می‌شه.