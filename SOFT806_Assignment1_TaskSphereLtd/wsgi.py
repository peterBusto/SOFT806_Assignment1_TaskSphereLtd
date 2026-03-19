"""
WSGI config for SOFT806_Assignment1_TaskSphereLtd project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SOFT806_Assignment1_TaskSphereLtd.settings')

application = get_wsgi_application()
