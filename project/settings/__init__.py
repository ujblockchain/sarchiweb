import os
from pathlib import Path

from decouple import Csv, config
from dotmap import DotMap
from split_settings.tools import include

# Init environment variables
ENV = DotMap({'config': config, 'Csv': Csv})

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Build paths inside the project directory
PROJECT_DIR = os.path.join(BASE_DIR, 'core/project')

# Secrete key
SECRET_KEY = ENV.config('SECRET_KEY')

# Admin path
ADMIN_PATH = ENV.config('ADMIN_PATH')

# Debug state
DEBUG = ENV.config('DEBUG', cast=bool)

# Include the base settings file
include(
    'base.py',
    'utils_config.py',
    'general_security.py',
    'admin_template_config.py',
)

# Include the environment-specific settings file based on the environment
if config('DJANGO_ENV') == 'Development' and DEBUG:
    include('development.py')
elif config('DJANGO_ENV') == 'Production':
    include('production.py')
