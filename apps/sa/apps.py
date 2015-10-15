import os
from django.apps import AppConfig

pages = []
admin_pages = [
    {'label': 'configs', 'view': 'v_configs', 'title': 'configs'},
    {'label': 'commands', 'view': 'v_commands', 'title': 'commands'},
    {'label': 'tables', 'view': 'v_tables', 'title': 'tables'},
]        

class appAppConfig(AppConfig):
    label = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    name = 'apps.{}'.format(label)
    verbose_name = ''
    pages = pages
    admin_pages = admin_pages
