from .base import *
import dj_database_url
from decouple import config
import os

SECRET_KEY = config('SECRET_KEY')
DEBUG= False
ALLOWED_HOSTS = ['.up.railway.app']
CSRF_TRUSTED_ORIGINS = ['https://*.up.railway.app']

DATABASES = {
    'default': dj_database_url.config(
        default = config('DB_URL'),
    )
}

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'