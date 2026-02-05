from project.settings import ADMIN_PATH, ENV

# general security settings in all environment
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# axes settings
SILENCED_SYSTEM_CHECKS = ENV.config('SILENCED_SYSTEM_CHECKS', cast=ENV.Csv())
AXES_FAILURE_LIMIT = ENV.config('AXES_FAILURE_LIMIT', cast=int)
AXES_COOLOFF_TIME = ENV.config('AXES_COOLOFF_TIME', cast=int)
AXES_ONLY_ADMIN_SITE = ENV.config('AXES_ONLY_ADMIN_SITE', cast=bool)
AXES_LOCKOUT_TEMPLATE = ENV.config('AXES_LOCKOUT_TEMPLATE')
AXES_LOCKOUT_URL = ENV.config('AXES_LOCKOUT_URL')
AXES_USERNAME_FORM_FIELD = ENV.config('AXES_USERNAME_FORM_FIELD')
AXES_RESET_ON_SUCCESS = ENV.config('AXES_RESET_ON_SUCCESS', cast=bool)
AXES_NEVER_LOCKOUT_WHITELIST = ENV.config('AXES_NEVER_LOCKOUT_WHITELIST', cast=bool)
AXES_IP_WHITELIST = ENV.config('AXES_IP_WHITELIST', cast=ENV.Csv())
AXES_ENABLE_ACCESS_FAILURE_LOG = ENV.config('AXES_ENABLE_ACCESS_FAILURE_LOG', cast=bool)
AXES_RESET_ON_SUCCESS = ENV.config('AXES_RESET_ON_SUCCESS', cast=bool)
AXES_LOCKOUT_PARAMETERS = ENV.config('AXES_LOCKOUT_PARAMETERS', cast=ENV.Csv())

# captcha settings
RECAPTCHA_PUBLIC_KEY = ENV.config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = ENV.config('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_REQUIRED_SCORE = ENV.config('RECAPTCHA_REQUIRED_SCORE', cast=float)

# csp default settings
CSP_DEFAULT_SRC = ("'none'",)
CSP_SCRIPT_SRC = (
    "'self'",
    'https://google.com',
    'https://www.googletagmanager.com',
    'https://gstatic.com',
    'https://ajax.googleapis.com',
    'https://www.google.com',
    'https://www.gstatic.com',
    "'unsafe-inline'",
)
CSP_FONT_SRC = (
    "'self'",
    'https://fonts.gstatic.com',
    'https://use.fontawesome.com',
    'data:',
)
CSP_STYLE_SRC = (
    "'self'",
    'https://google.com',
    'https://www.googletagmanager.com',
    'https://gstatic.com',
    'https://fonts.googleapis.com',
    'https://use.fontawesome.com',
    "'unsafe-inline'",
)
CSP_CONNECT_SRC = ("'self'", 'https://www.google-analytics.com')
CSP_MANIFEST_SRC = ("'self'",)
CSP_FRAME_SRC = ("'self'", 'https://www.google.com')
CSP_IMG_SRC = ("'self'", 'data:', 'https://www.googletagmanager.com')
CSP_MEDIA_SRC = ("'self'",)
CSP_FORM_ACTION = ("'self'",)
CSP_BASE_URI = "'self'"
CSP_FRAME_ANCESTORS = "'none'"
CSP_EXCLUDE_URL_PREFIXES = f'/{ADMIN_PATH}/'
CSP_REPORT_URI = ENV.config('SENTRY_REPORT_URL')

# logout inactivity
AUTO_LOGOUT = {'IDLE_TIME': ENV.config('AUTO_LOGOUT_IDLE_TIME', cast=int)}

# import export permission
IMPORT_EXPORT_IMPORT_PERMISSION_CODE = 'import'
IMPORT_EXPORT_EXPORT_PERMISSION_CODE = 'export'
