import os
from pathlib import Path
from decouple import Csv, config
from dotmap import DotMap
from split_settings.tools import include

# init environment variables
ENV = DotMap({'config': config, 'Csv': Csv})
# init project variables
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
PROJECT_DIR = os.path.join(BASE_DIR, 'core/project')
SECRET_KEY = ENV.config('SECRET_KEY')
ADMIN_PATH = ENV.config('ADMIN_PATH')
DEBUG = ENV.config('DEBUG', cast=bool)

# include the base settings file
include(
    'base.py',
    'utils_config.py',
    'general_security.py',
    'admin_template_config.py',
)

# include the environment-specific settings file based on the environment
if config('DJANGO_ENV') == 'Development' and DEBUG:
    include('development.py')
elif config('DJANGO_ENV') == 'Production':
    include('production.py')
