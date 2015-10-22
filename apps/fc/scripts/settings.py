import os
import time
import logging

APPNAME = 'fc'
BASEDIR = os.path.join(os.path.dirname(__file__), '../../../')
TEXTDIR = os.path.join(BASEDIR, 'data/{}/plain/'.format(APPNAME))
JSONDIR = os.path.join(BASEDIR, 'data/{}/json/'.format(APPNAME))
ARCHDIR = os.path.join(BASEDIR, 'data/{}/arch/'.format(APPNAME))

CONFIGSDIR = os.path.join(BASEDIR, 'data/{}/configs/'.format(APPNAME))
oldconfigpath = os.path.join(CONFIGSDIR, 'old.json')
newconfigpath = os.path.join(CONFIGSDIR, 'new.json')
fabrics_connections_path = os.path.join(os.path.dirname(__file__), 'FabricConnection.json')
switches_connections_path = os.path.join(os.path.dirname(__file__), 'SwitchConnection.json')

CONNECTIONS = os.path.join(os.path.dirname(__file__), 'SwitchConnection.json')

logging.basicConfig(
    filename=None,
    level=logging.INFO,
    format='%(asctime)s %(module)s %(levelname)s %(message)s'
)

PROCESSES = 4 # number of processes for multiprocessing

F_COMMANDS = [
    ['zoneshow', 'zoneshow'],
    ['fabricshow', 'fabricshow'],
    ['agshow', 'agshow'],
]
S_COMMANDS = [
    ['switchshow', 'switchshow'],
    ['chassisshow', 'chassisshow'],
    ['version', 'version'],
    ['sfpshow', 'sfpshow -all'],
    ['trunkshow', 'trunkshow'],
    ['porttrunkarea', 'porttrunkarea --show trunk'],
    ['nsshow', 'nsshow -r -t'],
]
P_COMMANDS = [
    ['portshow', 'portshow'],
]


PARSERS = {
    'zoneshow': ['alias', 'zone'],
    'fabricshow': ['fswitch'],
    'agshow': ['agswitch'],
    'switchshow': ['switch', 'port'],
    'chassisshow': ['serial'],
    'version': ['version'],
    'nsshow': ['name'],
    'sfpshow': ['sfp'],
    'portshow': ['portshow']
}

MODELS = [
    ['alias', 'Alias', {'before_delete_all': True}],
    ['zone', 'Zone', {'before_delete_all': True}],
    ['serial', 'Serial', {'before_delete_all': True}],
    ['version', 'Version', {'before_delete_all': True}],
    ['switch', 'Switch', {'before_delete_all': True}],
    ['port', 'Port', {'before_delete_all': True}],
    ['portshow', 'Portshow', {'before_delete_all': True}],
    ['name', 'Name', {'before_delete_all': True}],
    ['sfp', 'Sfp', {'before_delete_all': True}],
    ['alias_status', 'AliasStatus', {'before_delete_all': True}],
    ['zone_status', 'ZoneStatus', {'before_delete_all': True}],
    ['link', 'Link', {'before_delete_all': True}],
    ['swport_alias', 'SwportAlias', {'before_delete_all': True}],
    ['alias_swport', 'AliasSwport', {'before_delete_all': True}],
    ['port_relation', 'PortRelation', {'before_delete_all': True}],
    ['path', 'Path', {'before_delete_all': True}],
    ['switch_common', 'SwitchCommon', {'before_delete_all': True}],
    ['port_common', 'PortCommon', {'before_delete_all': True}],
]
