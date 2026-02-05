from project.settings import DEBUG, ENV, SECRET_KEY  # type: ignore

SECRET_KEY = SECRET_KEY
ALLOWED_HOSTS = ENV.config('ALLOWED_HOSTS', cast=ENV.Csv())
DEBUG = DEBUG

# database
DATABASES = {
    'default': {
        'ENGINE': ENV.config('ENGINE'),
        'NAME': ENV.config('NAME'),
        'HOST': ENV.config('HOST'),
        'USER': ENV.config('USER'),
        'PASSWORD': ENV.config('PASSWORD'),
        'PORT': ENV.config('PORT'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# security settings in production environment
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
SESSION_COOKIE_NAME = '__Host-sessionid'
CSRF_COOKIE_NAME = '__Host-csrftoken'
SERVER_EMAIL = ENV.config('SERVER_EMAIL')

# captcha settings
RECAPTCHA_PUBLIC_KEY = ENV.config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = ENV.config('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_REQUIRED_SCORE = ENV.config('RECAPTCHA_REQUIRED_SCORE', cast=float)

# cors settings
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [
    'https://ujblockchain.co.za',
]
CSRF_TRUSTED_ORIGINS = [
    'https://ujblockchain.co.za',
]
CORS_ORIGIN_WHITELIST = [
    'https://ujblockchain.co.za',
]
