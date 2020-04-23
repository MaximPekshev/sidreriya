# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u0872810/data/www/sidreriaybelgorod.ru/sidreriya')
sys.path.insert(1, '/var/www/u0872810/data/sidreriya/lib/python3.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'sidreriya.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()