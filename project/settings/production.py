from project.settings import env

SECRET_KEY = env.get('SECRET_KEY')
ALLOWED_HOSTS = env.get('ALLOWED_HOSTS', cast="list")
DEBUG = env.get('DEBUG', cast='bool')

# database
DATABASES = {
    'default': {
        'ENGINE': env.get('ENGINE'),
        'NAME': env.get('NAME'),
        'HOST': env.get('HOST'),
        'USER': env.get('USER'),
        'PASSWORD': env.get('PASSWORD'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# security settings in production environment
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 15768000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
SESSION_COOKIE_NAME = '__Host-sessionid'
CSRF_COOKIE_NAME = '__Host-csrftoken'
SERVER_EMAIL = env.get('SERVER_EMAIL')

# captcha settings
RECAPTCHA_PUBLIC_KEY = env.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env.get('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_REQUIRED_SCORE = env.get('RECAPTCHA_REQUIRED_SCORE', cast='float')

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
