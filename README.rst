.. image:: https://blockchain.uj.ac.za/static/images/logo.png


=========
SARChI
=========

South Africa-Switzerland Bilateral Research Chair in Blockchain Technology (UJ Blockchain) 
aims to explore blockchain integrations with real-world applications and development in Agric food.


==========
Setup
==========

Set environment variable for Django Secret Key, Debug, Allowed Host, and Admin Path. 
Also add configuration for Database, Django Axes and Email with SMTP Host.

.. code-block:: bash

    SECRET_KEY = '...'
    DEBUG = ...
    ALLOWED_HOSTS = '...'
    ADMIN_PATH = '...'

    ENGINE = '...'
    NAME = '...'
    HOST = '...'
    USER = '...'
    PASSWORD = '...'
    PORT = '...'

    SILENCED_SYSTEM_CHECKS = '...'
    AXES_FAILURE_LIMIT = '...'
    AXES_COOLOFF_TIME = '...'
    AXES_ONLY_ADMIN_SITE = '...'
    AXES_LOCKOUT_TEMPLATE = '...'
    AXES_LOCKOUT_URL = '...'
    AXES_USERNAME_FORM_FIELD = '...'
    AXES_RESET_ON_SUCCESS = '...'
    AXES_NEVER_LOCKOUT_WHITELIST = '...'
    AXES_IP_WHITELIST = '...'
    AXES_ENABLE_ACCESS_FAILURE_LOG = '...'
    AXES_RESET_ON_SUCCESS = '...'
    AXES_LOCKOUT_PARAMETERS = '...'

    EMAIL_BACKEND = ''...'
    EMAIL_PORT = '...'
    EMAIL_HOST = '...'
    EMAIL_HOST_USER = '...'
    EMAIL_HOST_PASSWORD = '...'
    DEFAULT_FROM_EMAIL = '...'
    SERVER_EMAIL = '...'
    EMAIL_SUBJECT_PREFIX = '...'
    EMAIL_USE_TSL = '...'



Recaptcha Setup
----------------

Set *Google Recaptcha* public and private key in environment variables. 
Public and private key can be gotten from *https://developers.google.com/recaptcha/*. 
Ensure you use :emphasis:`reCAPTCHA v3`.

.. code-block:: bash

    RECAPTCHA_PUBLIC_KEY = '...'
    RECAPTCHA_PRIVATE_KEY = '...'
    RECAPTCHA_REQUIRED_SCORE = ...



Huey Setup
---------------

Setup huey distributed task processing using *greenlet* worker type. 
For greenlet to work, you need to setup a monkey patch that serves as a custom bootstrap script.

.. code-block:: bash

    HUEY = {
        'huey_class': 'huey.RedisHuey',  # Huey implementation to use.
        'name': config('NAME'),  # Use db name for huey.
        'results': True,  # Store return values of tasks.
        'store_none': False,  # If a task returns None, do not save to results.
        'immediate': False,
        'utc': True,  # Use UTC for all times internally.
        'blocking': True,  # Perform blocking pop rather than poll Redis.
        'connection': {
            'host': 'localhost',
            'port': 6379,
            'db': 0,
            'connection_pool': None,  # Definitely you should use pooling!
            # ... tons of other options, see redis-py for details.

            # huey-specific connection parameters.
            'read_timeout': 1,  # If not polling (blocking pop), use timeout.
            'url': None,  # Allow Redis config via a DSN.
        },
        'consumer': {
            'workers': 1,
            'worker_type': 'thread',
            'initial_delay': 0.1,  # Smallest polling interval, same as -d.
            'backoff': 1.15,  # Exponential backoff using this rate, -b.
            'max_delay': 10.0,  # Max possible polling interval, -m.
            'scheduler_interval': 1,  # Check schedule every second, -s.
            'periodic': True,  # Enable crontab feature.
            'check_worker_health': True,  # Enable worker health checks.
            'health_check_interval': 1,  # Check worker health every second.
        },
    }


Running Project
----------------

Setup
^^^^^^^^^^^

.. code-block:: bash

    make setup


create Superuser
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    make superuser


Run Server
^^^^^^^^^^^
.. code-block:: bash

    make runserver


Start Background Task
^^^^^^^^^^^^^^^^^^^^^^^^^^

There is need for a background task using huey to send emails to users.

.. code-block:: bash
    $ make huey


Running Test With Coverage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash
    $ make run-coverage
