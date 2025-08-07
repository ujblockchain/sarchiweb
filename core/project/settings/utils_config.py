import jinja2
import sentry_sdk

from core.project.settings import BASE_DIR, ENV, PROJECT_DIR  # type: ignore

TEMPLATES = [
    {
        # Jinja2 template setup
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [f'{BASE_DIR}/core/jinja2'],
        'APP_DIRS': True,
        'OPTIONS': {
            'autoescape': False,
            'undefined': jinja2.StrictUndefined,
            'environment': 'core.project.settings.jinja.env.JinjaEnvironment',
            'extensions': [
                'jinja2.ext.loopcontrols',
                'jinja2.ext.do',
                'core.project.settings.jinja.extensions.DjangoNow',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [f'{BASE_DIR}/core/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = f'{BASE_DIR}/core/static'
STATICFILES_DIRS = [f'{PROJECT_DIR}/static']
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = f'{BASE_DIR}/core/media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings
EMAIL_BACKEND = ENV.config('EMAIL_BACKEND')
EMAIL_HOST = ENV.config('EMAIL_HOST')
EMAIL_PORT = ENV.config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = ENV.config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = ENV.config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = ENV.config('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = ENV.config('SERVER_EMAIL')
EMAIL_SUBJECT_PREFIX = ENV.config('EMAIL_SUBJECT_PREFIX')
EMAIL_USE_TLS = ENV.config('EMAIL_USE_TLS', cast=bool)
EMAIL_USE_SSL = ENV.config('EMAIL_USE_SSL', cast=bool)

# Add reversion settings
ADD_REVERSION_ADMIN = True
REVERSION_COMPARE_FOREIGN_OBJECTS_AS_ID = False
REVERSION_COMPARE_IGNORE_NOT_REGISTERED = False

# Sentry config
sentry_sdk.init(
    dsn=ENV.config('SENTRY_DNS'),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

# settings.py
HUEY = {
    'huey_class': 'huey.RedisHuey',
    'name': ENV.config('NAME'),
    'results': True,
    'store_none': False,
    'immediate': False,
    'utc': True,
    'blocking': True,
    'connection': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'connection_pool': None,
        'read_timeout': 1,
        'url': None,
    },
    'consumer': {
        'workers': 200,
        'worker_type': 'greenlet',
        'initial_delay': 0.1,
        'backoff': 1.15,
        'max_delay': 10.0,
        'scheduler_interval': 1,
        'periodic': True,
        'check_worker_health': True,
        'health_check_interval': 1,
    },
}
