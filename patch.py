# !/usr/bin/env python
import os
import sys

# Apply monkey-patch if we are running the huey consumer.
if 'djangohuey' in sys.argv:
    from gevent import monkey
    monkey.patch_all()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)