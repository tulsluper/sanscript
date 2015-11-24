import os
from django.apps import AppConfig


def samevalues(names):
    records = []
    for name in names: 
        if type(name) == str:
            records.append({key: name for key in ['label', 'model', 'title']})
    return records


pages = [
    {'label': 'switches', 'view': 'switches', 'title': 'Switches'},
    {'label': 'ports', 'view': 'ports', 'title': 'Ports'},
    {'label': 'aliases', 'view': 'aliases', 'title': 'Aliases'},
    {'label': 'zones', 'view': 'zones', 'title': 'Zones'},
    {'label': 'paths', 'view': 'paths', 'title': 'Paths'},
    {'label': 'changes', 'view': 'changes', 'title': 'Changes'},
    {'label': 'change_acknowledge', 'view': 'change_acknowledge', 'title': ''},
    {'label': 'stat', 'view': 'stat', 'title': ''},
    {'label': 'portlog', 'view': 'portlog', 'title': 'Portlog'},
]

commands = [
    {'label': 'test_connections', 'view': 'command', 'title': 'Test connections'},
    {'label': 'collect_data', 'view': 'command', 'title': 'Collect data'},
    {'label': 'collect_changes', 'view': 'command', 'title': 'Collect changes'},
]

config_models = samevalues([
    'FabricConnection',
    'SwitchConnection',
])

show_models = samevalues([
    'FabricConnection',
    'SwitchConnection',
    'Serial',
    'Version',
    'Switch',
    'Port',
    'Portshow',
    'Name',
    'Sfp',
    'Zone',
    'Alias',
    'AliasStatus',
    'ZoneStatus',
    'Link',
    'SwportAlias',
    'AliasSwport',
    'PortRelation',
    'Path',
    'Portlog',
    'Fabriclog',
    'Change',
    'Portlog',
    'Fabriclog',
])

class appAppConfig(AppConfig):
    label = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    name = 'apps.{}'.format(label)
    verbose_name = 'Switches'
    pages = pages
    commands = commands
    config_models = config_models
    show_models = show_models
