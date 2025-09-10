"""
ASGI config for VentaLibros project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VentaLibros.settings')

application = get_asgi_application()
