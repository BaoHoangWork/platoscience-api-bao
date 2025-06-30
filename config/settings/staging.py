from .base import *
import dj_database_url

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

ALLOWED_HOSTS = ['https://plato-api.onrender.com/']

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}

DEBUG = False

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'