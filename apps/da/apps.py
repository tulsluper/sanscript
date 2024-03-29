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
    {'label': 'capacity', 'view': 'capacity', 'title': 'Capacity'},
    {'label': 'capacity_history', 'view': 'capacity_history', 'title': 'Capacity History'},
    {'label': 'pd_types_capacity', 'view': 'pd_types_capacity', 'title': 'PD Capacity'},
    {'label': 'pd_types_quantity', 'view': 'pd_types_quantity', 'title': 'PD Quantity'},
    {'label': 'capacity_3par', 'view': 'capacity_3par', 'title': '3PAR Capacity'},
    {'label': 'capacity_3par_history', 'view': 'capacity_3par_history', 'title': '3PAR Capacity History'},
    {'label': 'volumes', 'view': 'volumes', 'title': 'Volumes'},
    {'label': 'hosts', 'view': 'hosts', 'title': 'Hosts'},
    {'label': 'hosts_capacity', 'view': 'hosts_capacity', 'title': 'HostsCapacity'},
    {'label': 'hosts_capacity_history', 'view': 'hosts_capacity_history', 'title': 'HostsCapacityHistory'},
    {'label': 'changes', 'view': 'changes', 'title': 'Changes'},
    {'label': 'change_acknowledge', 'view': 'change_acknowledge', 'title': ''},
    {'label': 'change_delete', 'view': 'change_delete', 'title': ''},
]

commands = [
    {'label': 'test_connections', 'title': 'Test connections'},
    {'label': 'collect_data', 'title': 'Collect data'},
]

config_models = samevalues([
    'StorageConnection',
])

show_models = samevalues([
    'StorageConnection',
    'Capacity',
    'CapacityHistory',
    'TPARCapacity',
    'TPARCapacityHistory',
    'PDTypesCapacity',
    'PDTypesQuantity',
    'TPARHost',
    'TPARVV',
    'TPARVLUN',
    'EVAVdisk',
    'EVAHost',
    'HDSHost',
    'HDSLU',
    'HDSMap',
    'Volume',
    'Host',
    'HostCapacity',
    'HostCapacityHistory',
    'VolumeChange',
])


class appAppConfig(AppConfig):
    label = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    name = 'apps.{}'.format(label)
    verbose_name = 'Storages'
    pages = pages
    commands = commands
    config_models = config_models
    show_models = show_models
