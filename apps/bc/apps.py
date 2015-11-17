import os
from django.apps import AppConfig


def samevalues(names):
    records = []
    for name in names:
        if type(name) == str:
            records.append({key: name for key in ['label', 'model', 'title']})
    return records


pages = [
    {'label': 'port', 'view': 'port_view', 'title': 'Port'},
    {'label': 'counter', 'view': 'counter_view', 'title': 'Counter'},
    {'label': 'select', 'view': 'select_view', 'title': 'Select'},
]
commands = [
    {'label': 'test_connections', 'view': 'command', 'title': 'Test connections'},
    {'label': 'collect_data', 'view': 'command', 'title': 'Collect data', 'enabled': False},
]
config_models = samevalues([
    'SwitchConnection',
    'CounterOid',
])
show_models = samevalues([
    'SwitchConnection',
    'XTimes',
    'Deltas',
    'CDicts',
    'PDicts',
    'SDicts',
    'Integers',
    'PortConfig',
])



class appAppConfig(AppConfig):
    label = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    name = 'apps.{}'.format(label)
    verbose_name = 'BCounters'
    pages = pages
    commands = commands
    config_models = config_models
    show_models = show_models
