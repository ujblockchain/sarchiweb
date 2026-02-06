from project.settings import env

ADMIN_PATH = env.get('ADMIN_PATH')

# General security settings in all environment
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Axes Settings
SILENCED_SYSTEM_CHECKS = env.get('SILENCED_SYSTEM_CHECKS', cast='list')
AXES_FAILURE_LIMIT = env.get('AXES_FAILURE_LIMIT', cast='int')
AXES_COOLOFF_TIME = env.get('AXES_COOLOFF_TIME', cast='int')
AXES_LOCKOUT_PARAMETERS = env.get('AXES_LOCKOUT_PARAMETERS', cast='list')
AXES_RESET_ON_SUCCESS = env.get('AXES_RESET_ON_SUCCESS', cast='bool')
AXES_IP_WHITELIST = env.get('AXES_IP_WHITELIST', cast='list', default=[])
AXES_USERNAME_FORM_FIELD = env.get('AXES_USERNAME_FORM_FIELD')
AXES_LOCKOUT_TEMPLATE = env.get('AXES_LOCKOUT_TEMPLATE')
AXES_LOCKOUT_URL = env.get('AXES_LOCKOUT_URL')
AXES_ENABLE_ACCESS_FAILURE_LOG = env.get('AXES_ENABLE_ACCESS_FAILURE_LOG', cast='bool')
AXES_IPWARE_META_PRECEDENCE_ORDER = env.get(
    'AXES_IPWARE_META_PRECEDENCE_ORDER', cast='list'
)

# Captcha settings
RECAPTCHA_PUBLIC_KEY = env.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env.get('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_REQUIRED_SCORE = env.get('RECAPTCHA_REQUIRED_SCORE', cast='float')

CSP_DEFAULT_SRC = ("'none'",)

CSP_SCRIPT_SRC = (
    "'self'",
    'https://cdn.tailwindcss.com',
    'https://cdn.jsdelivr.net',
    'https://unpkg.com',
    'https://cdnjs.cloudflare.com',
    'https://www.googletagmanager.com',
    'https://www.google.com',
    'https://www.gstatic.com',
    'https://ajax.googleapis.com',
    "'unsafe-inline'",
    "'unsafe-eval'",
)

CSP_FONT_SRC = (
    "'self'",
    'https://fonts.gstatic.com',
    'https://use.fontawesome.com',
    'https://cdnjs.cloudflare.com',
    'data:',
)

CSP_STYLE_SRC = (
    "'self'",
    'https://cdn.tailwindcss.com',
    'https://fonts.googleapis.com',
    'https://unpkg.com',
    'https://cdnjs.cloudflare.com',
    'https://cdn.jsdelivr.net',
    "'unsafe-inline'",
)

CSP_CONNECT_SRC = (
    "'self'",
    'https://cdn.jsdelivr.net',
    'https://www.google-analytics.com',
)

CSP_MANIFEST_SRC = ("'self'",)

CSP_FRAME_SRC = (
    "'self'",
    'https://www.google.com',
    'https://www.youtube.com',
    'https://youtube.com',
)

CSP_IMG_SRC = (
    "'self'",
    'https://cdn.jsdelivr.net',
    'https://www.googletagmanager.com',
    'data:',
    'https://*.tile.openstreetmap.org',
    'https://tile.openstreetmap.org',
    'https://source.unsplash.com',
    'https://images.unsplash.com',
)

CSP_MEDIA_SRC = ("'self'",)
CSP_FORM_ACTION = ("'self'",)
CSP_BASE_URI = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)
CSP_REPORT_URI = env.get('SENTRY_REPORT_URL')

# logout inactivity
AUTO_LOGOUT = {'IDLE_TIME': env.get('AUTO_LOGOUT_IDLE_TIME', cast='int')}

# NH3 settings
NH3_ALLOWED_TAGS = env.get('NH3_ALLOWED_TAGS')
NH3_ALLOWED_ATTRIBUTES = env.get('NH3_ALLOWED_ATTRIBUTES')
