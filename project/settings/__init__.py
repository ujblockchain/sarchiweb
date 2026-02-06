import os
from pathlib import Path
from split_settings.tools import include
from dotenv import load_dotenv

load_dotenv()

# init project variables
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_DIR = os.path.join(BASE_DIR, 'project')


class Env:
    @staticmethod
    def get(key: str, default=None, cast=None):
        value = os.getenv(key)
        if value is None:
            return default

        if cast == 'bool':
            val = str(value).lower().strip()
            return val in ('true',)
        elif cast == 'int':
            try:
                return int(value)
            except (ValueError, TypeError):
                return default
        elif cast == 'float':
            try:
                return float(value)
            except (ValueError, TypeError):
                return default
        elif cast == 'list':
            return [item.strip() for item in str(value).split(',') if item.strip()]
        else:
            return value


env = Env()

# include the base settings file
include(
    'base.py',
    'utils_config.py',
    'general_security.py',
    'admin_template_config.py',
)

# include the environment-specific settings file based on the environment
if env.get('DJANGO_ENV') == 'Development' and env.get('DEBUG', cast='bool'):
    include('development.py')
elif env.get('DJANGO_ENV') == 'Production':
    include('production.py')
