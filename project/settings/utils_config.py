import jinja2
import sentry_sdk
from project.settings import BASE_DIR, ENV, PROJECT_DIR

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [f'{BASE_DIR}/core/jinja2'],
        'APP_DIRS': True,
        'OPTIONS': {
            'autoescape': False,
            'undefined': jinja2.StrictUndefined,
            'environment': 'project.settings.jinja.env.JinjaEnvironment',
            'extensions': [
                'jinja2.ext.loopcontrols',
                'jinja2.ext.do',
                'project.settings.jinja.extensions.DjangoNow',
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

# static files (css, javascript, images)
STATIC_URL = 'static/'
STATIC_ROOT = f'{BASE_DIR}/core/static'
STATICFILES_DIRS = [f'{PROJECT_DIR}/static']
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# media files
MEDIA_URL = '/media/'
MEDIA_ROOT = f'{BASE_DIR}/core/media'

# default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# email settings
EMAIL_BACKEND = ENV.config('EMAIL_BACKEND')
EMAIL_PORT = ENV.config('EMAIL_PORT')
EMAIL_HOST = ENV.config('EMAIL_HOST')
EMAIL_HOST_USER = ENV.config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = ENV.config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = ENV.config('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = ENV.config('SERVER_EMAIL')
EMAIL_SUBJECT_PREFIX = ENV.config('EMAIL_SUBJECT_PREFIX')
EMAIL_USE_TSL = ENV.config('EMAIL_USE_TSL')


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
