import os
from .base import *

DEBUG = False

if SECRET_KEY == 'dev-unsafe-default':
    raise RuntimeError('DJANGO_SECRET_KEY missing')

_hosts = os.getenv('DJANGO_ALLOWED_HOSTS')
if not _hosts:
    raise RuntimeError('DJANGO_ALLOWED_HOSTS missing')
ALLOWED_HOSTS = [h.strip() for h in _hosts.split(',') if h.strip()]
CSRF_TRUSTED_ORIGINS = [f"https://{h.lstrip('.')}" for h in ALLOWED_HOSTS if not h.startswith('.')]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
        'file': {'class': 'logging.FileHandler', 'filename': '/var/log/inventario/app.log'},
    },
    'loggers': {
        'django': {'handlers': ['console', 'file'], 'level': 'INFO'},
        'inventory.movements': {'handlers': ['console', 'file'], 'level': 'INFO'},
    },
}

