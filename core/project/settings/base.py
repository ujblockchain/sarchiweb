from core.project.settings import ADMIN_PATH

# Allowed Host
ALLOWED_HOSTS = ['blockchain.uj.ac.za']

# Admin path
ADMIN_PATH = ADMIN_PATH

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
    'huey.contrib.djhuey',
    'anymail',
    # app
    'core.account.apps.AccountConfig',
    'core.blog.apps.BlogConfig',
    'core.bootcamps.apps.BootcampsConfig',
    'core.contact.apps.ContactConfig',
    'core.events.apps.EventsConfig',
    'core.facilitators.apps.FacilitatorsConfig',
    'core.masterclass.apps.MasterclassConfig',
    'core.newsletters.apps.NewslettersConfig',
    'core.pages.apps.PagesConfig',
    'core.partners.apps.PartnersConfig',
    'core.program.apps.ProgramConfig',
    'core.repository.apps.RepositoryConfig',
    'core.sms.apps.SmsConfig',
    # third party apps by location
    'django_prose_editor',
    'import_export',
    'django_cleanup.apps.CleanupConfig',
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
    # custom csp
    'core.project.settings.middleware.custom_csp.CustomCSPMiddleware',
    # Remote Address Middleware, useful for security
    'core.project.settings.middleware.remoteAddr.RemoteAddrMiddleware',
    # Current User Middleware
    'core.project.settings.middleware.current_request.RequestMiddleware',
    # Logout
    'django_auto_logout.middleware.auto_logout',
    # AxesMiddleware should be the last middleware in the MIDDLEWARE list.
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'core.project.urls'

WSGI_APPLICATION = 'core.project.wsgi.application'

# Password validation
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

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Johannesburg'

USE_I18N = True

USE_TZ = True

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth Backend
AUTHENTICATION_BACKENDS = [
    # AxesStandaloneBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesStandaloneBackend',
    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]
