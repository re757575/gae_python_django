import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'gae_python_web.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
