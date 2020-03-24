"""
WSGI config for EinkaufsApp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.environ.get('DEBUG'):
    print("DEBUG-MODUS")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EinkaufsApp.settings_development')
else:
    print("PRODUCTION-MODUS")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EinkaufsApp.settings_production')

application = get_wsgi_application()
