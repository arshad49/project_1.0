"""
WSGI config for dental_clinic_rag project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dental_clinic_rag.settings')
application = get_wsgi_application()
