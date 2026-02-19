import jinja2
import sentry_sdk
from import_export.formats.base_formats import CSV, XLSX
from project.settings import BASE_DIR, env, PROJECT_DIR

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [f'{BASE_DIR}/jinja2'],
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
        'DIRS': [f'{BASE_DIR}/templates'],
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
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [f'{PROJECT_DIR}/static']

# default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# email settings
ANYMAIL = {"MAILTRAP_API_TOKEN": env.get('MAILTRAP_API_TOKEN')}
EMAIL_BACKEND = env.get('EMAIL_BACKEND')
DEFAULT_FROM_EMAIL = env.get('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = env.get('SERVER_EMAIL')
EMAIL_SUBJECT_PREFIX = env.get('EMAIL_SUBJECT_PREFIX', default='UJBlockchain')

# Sentry config
sentry_sdk.init(
    dsn=env.get('SENTRY_DNS'),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

IMPORT_FORMATS = [CSV, XLSX]
EXPORT_FORMATS = [CSV, XLSX]
IMPORT_EXPORT_IMPORT_IGNORE_BLANK_LINES = env.get(
    'IMPORT_EXPORT_IMPORT_IGNORE_BLANK_LINES', cast='bool'
)
IMPORT_EXPORT_ESCAPE_FORMULAE_ON_EXPORT = env.get(
    'IMPORT_EXPORT_ESCAPE_FORMULAE_ON_EXPORT', cast='bool'
)
IMPORT_EXPORT_IMPORT_PERMISSION_CODE = env.get('IMPORT_EXPORT_IMPORT_PERMISSION_CODE')
IMPORT_EXPORT_EXPORT_PERMISSION_CODE = env.get('IMPORT_EXPORT_EXPORT_PERMISSION_CODE')
