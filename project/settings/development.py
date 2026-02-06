from project.settings import env
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
if 'django_extensions' not in INSTALLED_APPS and 'debug_toolbar' not in INSTALLED_APPS:
    INSTALLED_APPS.insert(len(INSTALLED_APPS) - 2, 'django_extensions')
    INSTALLED_APPS.insert(len(INSTALLED_APPS) - 3, 'debug_toolbar')

# django debug middleware
if 'debug_toolbar.middleware.DebugToolbarMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(len(MIDDLEWARE) - 1, 'debug_toolbar.middleware.DebugToolbarMiddleware')

# set internal ips
INTERNAL_IPS = ['127.0.0.1']

# cors settings
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
]
