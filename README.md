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

### Django huey Setup
Setup huey distributed task processing using 'greenlet' worker type. For greenlet to work, you need to setup a money patch that serves as a custom bootstrap script.

```
DJANGO_HUEY = {
    'default': 'send_emails',  # this name must match with any of the queues defined below.
    'queues': {
        'send_emails': {
            'huey_class': 'huey.RedisHuey',
            'name': 'send_email_task', #name of task
            'immediate': False,
            'consumer': {
                'workers': 10,
                'worker_type': 'greenlet', # using greenlet worker type
            },
        },
    },
}

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

### Start Background Task
There is need for a background task using huey. Since the default task is set to 'send_emails' there is no need to add '--queue send_emails'
```
$ python manage.py djangohuey

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

