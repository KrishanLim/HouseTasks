from .base import *
import dj_database_url
from decouple import config
import os

SECRET_KEY = config('SECRET_KEY')
DEBUG= False
ALLOWED_HOSTS = [os.environ.get('RAILWAY_HOSTNAME', '')]

DATABASES = {
    'default': dj_database_url.config(
        default = config('DB_URL'),
    )
}

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'