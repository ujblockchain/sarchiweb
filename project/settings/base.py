from project.settings import env

ALLOWED_HOSTS = ['ujblockchain.co.za']
ADMIN_PATH = env.get('ADMIN_PATH')

INSTALLED_APPS = [
    # third party apps
    'django_daisy',
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    # third party apps
    'axes',
    'csp',
    'corsheaders',
    'django_recaptcha',
    'anymail',
    'phonenumber_field',
    # app
    'contact.apps.ContactConfig',
    'user.apps.UserConfig',
    # third party apps by location
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
    'django_prose_editor',
    'import_export',
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
    'project.settings.middleware.custom_csp.CustomCSPMiddleware',
    'project.settings.middleware.current_request.RequestMiddleware',
    'django_auto_logout.middleware.auto_logout',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

# password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Johannesburg'

USE_I18N = True

USE_TZ = True

# default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth Backend
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# site settings
SITE_ID = 1
# custom user
AUTH_USER_MODEL = 'user.Users'
