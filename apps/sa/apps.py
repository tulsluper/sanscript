import os
from django.apps import AppConfig

pages = [
    {'label': 'settings', 'view': 'settings_view', 'title': 'settings'},
]
admin_pages = [
    {'label': 'configs', 'view': 'v_configs', 'title': 'configs'},
    {'label': 'commands', 'view': 'v_commands', 'title': 'commands'},
    {'label': 'tables', 'view': 'v_tables', 'title': 'tables'},
]        

class appAppConfig(AppConfig):
    """
    | AppConfig for current application.
    | For more information see
    | https://docs.djangoproject.com/en/1.8/ref/applications/#application-configuration
    """

    label = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    name = 'apps.{}'.format(label)
    verbose_name = ''
    pages = pages
    admin_pages = admin_pages
