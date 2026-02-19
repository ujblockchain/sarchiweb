from project.settings import BASE_DIR, env
from project.settings.base import INSTALLED_APPS, MIDDLEWARE

SECRET_KEY = env.get('SECRET_KEY')
ALLOWED_HOSTS = env.get('ALLOWED_HOSTS', cast='list')
DEBUG = env.get('DEBUG')

# Database
DATABASES = {
    'default': {
        'ENGINE': env.get('ENGINE'),
        'NAME': env.get('NAME'),
        'HOST': env.get('HOST'),
        'USER': env.get('USER'),
        'PASSWORD': env.get('PASSWORD'),
        'PORT': env.get('PORT'),
    }
}

# installed app
# add django extension and debug toolbar
INSTALLED_APPS += ['django_extensions', 'debug_toolbar']

# django debug middleware
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

# set internal ips
INTERNAL_IPS = ['127.0.0.1']

# cors settings
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
]


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
