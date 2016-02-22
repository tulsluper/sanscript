import os
from django.apps import AppConfig
from django.apps import apps


def samevalues(names):
    records = []
    for name in names:
        if type(name) == str:
            records.append({key: name for key in ['label', 'model', 'title']})
    return records


pages = [
]

commands = [
    {'label': 'test_connections', 'title': 'Test connections'},
    {'label': 'collect_data', 'title': 'Collect data'},
]

config_models = samevalues([
    'Connection',
])

show_models = samevalues([
    'Enclosure',
    'Server',
    'Mezzanine',
])


class appAppConfig(AppConfig):
    label = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    name = 'apps.{}'.format(label)
    verbose_name = 'Enclosure'
    pages = pages
    commands = commands
    config_models = config_models
    show_models = show_models

