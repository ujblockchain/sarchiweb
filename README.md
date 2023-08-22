![image info](./sarchi/static/images/main-logo.png)

# SARCHI
South Africa-Switzerland Bilateral Research Chair in Blockchain Technology aims to explore blockchain integrations with real-world applications and development in Agric food.

## Setup
Set environment variable for Django Secret Key, Debug, Allowed Host, and Admin Path. Also set to work with SMTP Host for Email functionality.

```
SECRET_KEY = '...'
DEBUG = ..
ALLOWED_HOSTS = '...'
ADMIN_PATH = '..'

ENGINE = '...'
NAME = '...'
HOST = '...'
USER = '...'
PASSWORD = '...'
PORT = ...

EMAIL_BACKEND = ''...'
EMAIL_PORT = '...'
EMAIL_HOST = '...'
EMAIL_HOST_USER = '...'
EMAIL_HOST_PASSWORD = '...'
DEFAULT_FROM_EMAIL = '...'
SERVER_EMAIL = '...'
EMAIL_SUBJECT_PREFIX = '...'
EMAIL_USE_TSL = '...'

```

### Recaptcha Setup
Set google recaptcha public and private key in environment variables. Public and private key can be gotten from https://developers.google.com/recaptcha/. Ensure you use reCAPTCHA v3.

```
RECAPTCHA_PUBLIC_KEY = '...'
RECAPTCHA_PRIVATE_KEY = '...'
RECAPTCHA_REQUIRED_SCORE = ...

```

### Sentry Setup
Set sentry DNS path. DNS path can be gotten from https://sentry.io/welcome/. 

```
SENTRY_DNS= '...'

```

## Running Project

### Install Dependencies
```
$ pip install -r requirements.txt

```

### Make Migrations
```
$ python manage.py makemigrations
$ python manage.py migrate

```

### create Superuser

```
$ python manage.py createsuperuser

```

### Run Server
```
$ python manage.py runserver

```

## Running Test With Coverage
```
$ coverage run manage.py test

```

### Coverage Report
```
$ coverage report
$ coverage html

```

