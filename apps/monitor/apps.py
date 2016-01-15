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
    {'label': 'models', 'view': 'models_view', 'title': 'Models'},
    {'label': 'model_register', 'view': 'model_register', 'title': ''},
    {'label': 'model_edit', 'view': 'model_edit', 'title': ''},
    {'label': 'model_unregister', 'view': 'model_unregister', 'title': ''},
    {'label': 'rules', 'view': 'rules_view', 'title': 'Rules'},
    {'label': 'rule_delete', 'view': 'rule_delete_view', 'title': ''},
    {'label': 'rule_empty', 'view': 'rule_empty', 'title': ''},
    {'label': 'rule', 'view': 'rule_view', 'title': ''},
]

commands = [
    {'label': 'test_connections', 'title': 'Test connections'},
    {'label': 'collect_data', 'title': 'Collect data'},
]

config_models = samevalues([
    'ObjectItem',
    'TriggerItem',
])

show_models = samevalues([
    'Rule',
    'ObjectItem',
    'TriggerItem',
])


class appAppConfig(AppConfig):
    label = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    name = 'apps.{}'.format(label)
    verbose_name = 'Monitor'
    pages = pages
    commands = commands
    config_models = config_models
    show_models = show_models
