import os
import logging
from datetime import datetime

APPNAME = 'en'
BASEDIR = os.path.join(os.path.dirname(__file__), '../../../')
TEXTDIR = os.path.join(BASEDIR, 'data/{}/plain/'.format(APPNAME))
JSONDIR = os.path.join(BASEDIR, 'data/{}/json/'.format(APPNAME))
ARCHDIR = os.path.join(BASEDIR, 'data/{}/arch/'.format(APPNAME))
CONFIGSDIR = os.path.join(BASEDIR, 'data/{}/configs/'.format(APPNAME))

CONNECTIONS = os.path.join(os.path.dirname(__file__), 'Connection.json')


MODELS = [
    ['enclosures', 'Enclosure', {'before_delete_all': True}],
    ['servers', 'Server', {'before_delete_all': True}],
    ['mezzanines', 'Mezzanine', {'before_delete_all': True}],
]
