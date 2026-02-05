<figure align="center">
  <img src="https://ujblockchain.co.za/static/img/logo.png" alt="UJ Blockchain Logo" width="220"/>
  <figcaption>South Africa-Switzerland Bilateral Research Chair in Blockchain Technology</figcaption>
</figure>

# SARChI

South Africa-Switzerland Bilateral Research Chair in Blockchain Technology (University of Johannesburg – UJ Blockchain) focused on blockchain integration with **real-world applications**.

## Setup – Environment Variables

Create a `.env` file (or set these in your environment):

```bash
# core django settings
SECRET_KEY="your-very-long-random-secret-key"
DEBUG=True                # change to False in production
ALLOWED_HOSTS=".localhost,127.0.0.1,[::1],yourdomain.com"
ADMIN_PATH="admin"

# database
ENGINE="django.db.backends.postgresql"
NAME="sarchi_blockchain"
HOST="localhost"
USER="your_db_user"
PASSWORD="your_db_password"
PORT="5432"

# security / django axes (brute-force protection)
SILENCED_SYSTEM_CHECKS="axes.W004"
AXES_FAILURE_LIMIT=5
AXES_COOLOFF_TIME="00:30:00"
AXES_ONLY_ADMIN_SITE=True
AXES_LOCKOUT_TEMPLATE="axes/lockout.html"
AXES_LOCKOUT_URL="/locked/"
AXES_USERNAME_FORM_FIELD="username"
AXES_RESET_ON_SUCCESS=True
AXES_NEVER_LOCKOUT_WHITELIST=False
AXES_IP_WHITELIST="127.0.0.1, ::1"
AXES_ENABLE_ACCESS_FAILURE_LOG=True
AXES_LOCKOUT_PARAMETERS=["ip_address", "user_agent"]

# Email (SMTP)
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.your-provider.com"
EMAIL_PORT=587
EMAIL_HOST_USER="your@smtp.user"
EMAIL_HOST_PASSWORD="your-smtp-password"
DEFAULT_FROM_EMAIL="no-reply@yourdomain.com"
SERVER_EMAIL="no-reply@yourdomain.com"
EMAIL_SUBJECT_PREFIX="[SARChI] "
EMAIL_USE_TLS=True
EMAIL_USE_SSL=True
```

## reCAPTCHA v3 Setup

Get your site key and secret key from: `https://www.google.com/recaptcha/admin/create` (make sure to select **reCAPTCHA v3**) and to environment variables (e.g. `.env` file):

```bash
RECAPTCHA_PUBLIC_KEY="6LeIxAcT...your-public-key..."
RECAPTCHA_PRIVATE_KEY="6LeIxAcT...your-secret-key..."
RECAPTCHA_REQUIRED_SCORE=0.4
```

> **Note**: Google's official reCAPTCHA v3 documentation recommends starting with a threshold around **0.5** and then tuning it based on your actual traffic and risk patterns in the reCAPTCHA admin console.
>
> - Lower values (e.g. 0.3–0.4) → more permissive (fewer challenges, higher risk of bots)
> - Higher values (e.g. 0.7+) → stricter (more legitimate users may be challenged)

## Running the Project

### 1. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Create a superuser

```bash
python manage.py createsuperuser
```

### 3. Start development server

```bash
python manage.py runserver
```

### 4. Running tests + coverage

```bash
pip install coverage

# run tests and collect coverage data
coverage run --source='.' manage.py test

# view basic coverage summary in the terminal
coverage report

# generate detailed html report
coverage html
```
