"""
WSGI config for tibia_stats project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import dotenv

# dotenv settings
dotenv.load_dotenv(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tibia_stats.settings')

application = get_wsgi_application()
