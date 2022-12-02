from .settings import *
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpsaf')
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'
ALLOWED_HOSTS = [os.environ.get('DJANGO_ALLOW_HOSTS', '127.0.0.1')]
STATIC_URL = os.environ.get('DJANGO_STATIC_URL', 'static/')
STATIC_ROOT = os.path.join(BASE_DIR, os.environ.get('DJANGO_STATIC_ROOT', 'static'))
MEDIA_ROOT = os.path.join(BASE_DIR, os.environ.get('DJANGO_STATIC_ROOT', 'media'))


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get('DJANGO_DB_NAME', 'postgres'),
        "USER": os.environ.get('DJANGO_DB_USERNAME', 'postgres'),
        "PASSWORD": os.environ.get('DJANGO_DB_PASSWORD', 'postgres'),
        "HOST": "db",  # set in docker-compose.yml
        "PORT": 5432,  # default postgres port
    }
}
