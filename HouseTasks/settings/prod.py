from .base import *
import dj_database_url
from decouple import config
import os

SECRET_KEY = config('SECRET_KEY')
DEBUG= False
ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')]

DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.postgresql',
        'NAME' : config('DB_NAME'),
        'USER' : config('DB_USER'),
        'PASSWORD' : config('DB_PASSWORD'),
        'HOST' : config('DB_HOST'),
        'PORT' : config('DB_PORT'),
    }
}

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'