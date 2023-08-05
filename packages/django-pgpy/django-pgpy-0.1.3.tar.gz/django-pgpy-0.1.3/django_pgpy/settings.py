from django.conf import settings
from django_pgpy.defaults import get_default_restorers

DJANGO_PGPY_DEFAULT_RESTORERS = getattr(settings, 'DJANGO_PGPY_DEFAULT_RESTORERS', get_default_restorers)

DJANGO_PGPY_AES_KEY_LENGTH = 32
DJANGO_PGPY_RSA_KEY_LENGTH = 2048