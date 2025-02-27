# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u0872810/data/www/sidreriyabelgorod.ru/sidreriya')
sys.path.insert(1, '/var/www/u0872810/data/www/sidreriyabelgorod.ru/.venv/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'sidreriya.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()