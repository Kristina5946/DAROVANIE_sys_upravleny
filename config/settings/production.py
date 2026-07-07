"""Production на shared-хостинге reg.ru (Passenger + WhiteNoise)."""
from .base import *  # noqa: F401,F403

DEBUG = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# WhiteNoise — раздача статики без Nginx-настройки
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    *MIDDLEWARE[1:],
]

# Без CompressedManifest — на shared-хостинге collectstatic падает с "can't start new thread"
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.StaticFilesStorage',
    },
}
