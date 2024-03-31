import os
from pathlib import Path
from decouple import config, Csv
import jinja2
import sentry_sdk

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Project directory
PROJECT_DIR = Path(__file__).resolve().parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Allowed Host
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1', cast=Csv())

# Admin Path URL Name
ADMIN_PATH = config('ADMIN_PATH')

# Application definition
INSTALLED_APPS = [
    # third party apps
    'jazzmin',
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party apps
    'axes',
    'corsheaders',
    'django_recaptcha',
    'reversion',
    'reversion_compare',
    # ckeditor app
    'django_ckeditor_5',
    # huey
    'bx_django_utils',
    'huey_monitor',
    # app
    'account.apps.AccountConfig',
    'blog.apps.BlogConfig',
    'bootcamps.apps.BootcampsConfig',
    'contact.apps.ContactConfig',
    'facilitators.apps.FacilitatorsConfig',
    'newsletters.apps.NewslettersConfig',
    'pages.apps.PagesConfig',
    'partners.apps.PartnersConfig',
    'program.apps.ProgramConfig',
    'projects.apps.ProjectsConfig',
    'repository.apps.RepositoryConfig',
    'settings.apps.SettingsConfig',
    'sms.apps.SmsConfig',
    # third party apps by location
    'import_export',
    'django_cleanup.apps.CleanupConfig',
    'django_huey',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # CSP
    'csp.middleware.CSPMiddleware',
    # Remote Address Middleware, useful for security
    'sarchi.middleware.remoteAddr.RemoteAddrMiddleware',
    # Current User Middleware
    'sarchi.middleware.current_request.RequestMiddleware',
    # AxesMiddleware should be the last middleware in the MIDDLEWARE list.
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'sarchi.urls'

TEMPLATES = [
    {
        # Jinja2 template setup
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'jinja2')],
        'APP_DIRS': True,
        'OPTIONS': {
            'autoescape': False,
            'undefined': jinja2.StrictUndefined,
            'environment': 'sarchi.jinja.env.JinjaEnvironment',
            'extensions': [
                'jinja2.ext.loopcontrols',
                'jinja2.ext.do',
                'sarchi.jinja.extensions.DjangoNow',
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'sarchi.wsgi.application'

# Set Django Extension nd Debug Toolbar for development environment
if DEBUG:
    # update installed apps
    local_env_apps = ['django_extensions', 'debug_toolbar']
    for i in range(len(local_env_apps)):
        INSTALLED_APPS.insert(31 + i, local_env_apps[i])

    # update middleware with debug tool bar
    MIDDLEWARE.insert(7, 'debug_toolbar.middleware.DebugToolbarMiddleware')

    # set internal ips
    INTERNAL_IPS = ['127.0.0.1']

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config('ENGINE'),
        'NAME': config('NAME'),
        'HOST': config('HOST'),
        'USER': config('USER'),
        'PASSWORD': config('PASSWORD'),
        'PORT': config('PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Johannesburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTHENTICATION_BACKENDS = [
    # AxesStandaloneBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesStandaloneBackend',
    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(PROJECT_DIR, 'static')]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# email settings
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = config('SERVER_EMAIL')
EMAIL_SUBJECT_PREFIX = config('EMAIL_SUBJECT_PREFIX')
EMAIL_USE_TSL = config('EMAIL_USE_TSL')

# Security Settings In Production Environment
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
if DEBUG == False:
    # security settings
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 15768000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SECURE_REFERRER_POLICY = 'same-origin'
    SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
    # Prefix session cookie with '__Host-'
    SESSION_COOKIE_NAME = '__Host-sessionid'
    # Prefix CSRF cookie with '__Host-'
    CSRF_COOKIE_NAME = '__Host-csrftoken'

# Cors settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
]

# Axes Settings
SILENCED_SYSTEM_CHECKS = config('SILENCED_SYSTEM_CHECKS', cast=Csv())
# Number of failed login before block
AXES_FAILURE_LIMIT = config('AXES_FAILURE_LIMIT', cast=int)
# Time to wait after lockout(hrs)
AXES_COOLOFF_TIME = config('AXES_COOLOFF_TIME', cast=int)
# Enable security lockout only for admin site
AXES_ONLY_ADMIN_SITE = config('AXES_ONLY_ADMIN_SITE', cast=bool)
# lockout template
AXES_LOCKOUT_TEMPLATE = config('AXES_LOCKOUT_TEMPLATE')
# Lockout url path
AXES_LOCKOUT_URL = config('AXES_LOCKOUT_URL')
# Form field that contains your users usernames.
AXES_USERNAME_FORM_FIELD = config('AXES_USERNAME_FORM_FIELD')
# Reset after success login
AXES_RESET_ON_SUCCESS = config('AXES_RESET_ON_SUCCESS', cast=bool)
# Whitelist local host
AXES_NEVER_LOCKOUT_WHITELIST = config('AXES_NEVER_LOCKOUT_WHITELIST', cast=bool)
AXES_IP_WHITELIST = config('AXES_IP_WHITELIST', cast=Csv())
# Enable writing login failure logs to database
AXES_ENABLE_ACCESS_FAILURE_LOG = config('AXES_ENABLE_ACCESS_FAILURE_LOG', cast=bool)
# Successful login will reset the number of failed logins
AXES_RESET_ON_SUCCESS = config('AXES_RESET_ON_SUCCESS', cast=bool)
# lock user using ip address, username and user agent
AXES_LOCKOUT_PARAMETERS = config('AXES_LOCKOUT_PARAMETERS', cast=Csv())

# captcha settings
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_REQUIRED_SCORE = config('RECAPTCHA_REQUIRED_SCORE', cast=float)

# CSP default settings
CSP_DEFAULT_SRC = "'none'"
CSP_SCRIPT_SRC = (
    "'self'",
    'https://www.google.com',
    'https://www.googletagmanager.com',
    'https://www.gstatic.com',
)
CSP_FONT_SRC = (
    "'self'",
    'https://fonts.gstatic.com',
    'https://use.fontawesome.com',
    'https://fonts.gstatic.com',
)
CSP_FORM_ACTION = ["'self'"]  # Allow form submissions to URLs from the same origin
CSP_BASE_URI = ["'none'"]  # Disallow base URLs from the same origin
CSP_FRAME_ANCESTORS = ["'none'"]
# exclude admin path
CSP_EXCLUDE_URL_PREFIXES = f'/{ADMIN_PATH}/'

# Add reversion settings
## add admin interface
ADD_REVERSION_ADMIN = True
## compare by id
REVERSION_COMPARE_FOREIGN_OBJECTS_AS_ID = False
## ignore not registered in comparison
REVERSION_COMPARE_IGNORE_NOT_REGISTERED = False

# import jazzmin settings
from .configuration.admin.jazzdmin import *

# import ck editor settings
from .configuration.admin.ckeditor import *


# sentry config
sentry_sdk.init(
    dsn=config('SENTRY_DNS'),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

# huey distributed task processing
DJANGO_HUEY = {
    'default': 'send_emails',  # this name must match with any of the queues defined below.
    'queues': {
        'send_emails': {  # this name will be used in decorators below
            'huey_class': 'huey.RedisHuey',
            'name': 'send_email_task',  # name of task
            'immediate': False,
            'consumer': {
                'workers': 10,
                'worker_type': 'greenlet',  # using greenlet worker type
            },
        },
        'bootcamp_reminder_emails': {  # this name will be used in decorators below
            'huey_class': 'huey.RedisHuey',
            'name': 'bootcamp_reminder_email_task',  # name of task
            'immediate': False,
            'consumer': {
                'workers': 10,
                'worker_type': 'greenlet',  # using greenlet worker type
            },
        },
        'send_sms': {
            'huey_class': 'huey.RedisHuey',
            'name': 'send_sms_task',  # name of task
            'immediate': False,
            'consumer': {
                'workers': 10,
                'worker_type': 'greenlet',  # using greenlet worker type
            },
        },
    },
}
