<figure align="center">
  <img src="https://ujblockchain.co.za/static/img/logo.png" alt="UJ Blockchain Logo" width="220"/>
  <figcaption>South Africa-Switzerland Bilateral Research Chair in Blockchain Technology</figcaption>
</figure>

# SARChI

South Africa-Switzerland Bilateral Research Chair in Blockchain Technology (University of Johannesburg – UJ Blockchain) focused on blockchain integration with **real-world applications**.

## Setup – Environment Variables

Create a `.env` file (or set these in your environment):

```bash
SECRET_KEY = '...'
ALLOWED_HOSTS = '...'
DEBUG = ...
DJANGO_ENV = ...
ADMIN_PATH = ...
AUTO_LOGOUT_IDLE_TIME = ...


# database
ENGINE = '...'
NAME = ...
HOST = ...
USER = ...
PASSWORD = ...
PORT = ...

# email
EMAIL_BACKEND = '...'
EMAIL_PORT = ...
MAILTRAP_API_TOKEN = ...
EMAIL_HOST = '...'
EMAIL_HOST_USER = '...'
EMAIL_HOST_PASSWORD = '...'
DEFAULT_FROM_EMAIL = '...'
SERVER_EMAIL = '...'
EMAIL_SUBJECT_PREFIX = '...'
EMAIL_USE_TSL = ...


#captcha seetings
RECAPTCHA_PUBLIC_KEY = '...'
RECAPTCHA_PRIVATE_KEY = '...'
RECAPTCHA_REQUIRED_SCORE = ...

#sentry
SENTRY_DNS = '...'
SENTRY_REPORT_URL = '...'


# csp
SECURE_SSL_HOST = ...
CSRF_TRUSTED_ORIGINS = '....'

# axes settings
SILENCED_SYSTEM_CHECKS = '...'
AXES_IPWARE_PROXY_COUNT = 1
AXES_IPWARE_META_PRECEDENCE_ORDER = '...'
AXES_LOCKOUT_PARAMETERS = '...'
AXES_FAILURE_LIMIT = ...
AXES_COOLOFF_TIME = ...
AXES_RESET_ON_SUCCESS = ...
AXES_ENABLE_ACCESS_FAILURE_LOG = ...
AXES_USERNAME_FORM_FIELD = ...
AXES_LOCKOUT_TEMPLATE = '...'
AXES_LOCKOUT_URL = '...'

# NH3 settings
NH3_ALLOWED_TAGS = '...'
NH3_ALLOWED_ATTRIBUTES = '...'


# django import/export
IMPORT_EXPORT_IMPORT_IGNORE_BLANK_LINES = ...
IMPORT_EXPORT_ESCAPE_FORMULAE_ON_EXPORT = ...
IMPORT_EXPORT_IMPORT_PERMISSION_CODE = ...
IMPORT_EXPORT_EXPORT_PERMISSION_CODE = ...

```

## reCAPTCHA v3 Setup

Get your site key and secret key from: `https://www.google.com/recaptcha/admin/create` (make sure to select **reCAPTCHA v3**) and add to environment variables (e.g. `.env` file):

```bash
RECAPTCHA_PUBLIC_KEY ='....'
RECAPTCHA_PRIVATE_KEY ='...'
RECAPTCHA_REQUIRED_SCORE = '...'
```

## Running the Project

### Apply migrations

```bash
make migrations
make migrate 
# or 
# python manage.py makemigrations
# python manage.py migrate
```

### Create a superuser

```bash
make makesuperuser # python manage.py createsuperuser
```

### Setup OTP
Since an OTP is required to login to `Admin`, you need to setup an initial OTP before you can setup in the Admin.

```bash
python manage.py addstatictoken <your_username_which_is_the_email_used_to_create_superuser>
```


### Start development server

```bash
make runserver # or python manage.py runserver
```

### Running tests 

```bash
make coverage-test # or python manage.py test
```
