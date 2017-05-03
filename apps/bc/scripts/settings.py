"""
"""
import os

APPNAME = 'bc'
BASEDIR = os.path.join(os.path.dirname(__file__), '../../../')
DATADIR = os.path.join(BASEDIR, 'data/{}'.format(APPNAME))
JSONDIR = os.path.join(DATADIR, 'json')
TEMPFILE = os.path.join(JSONDIR, 'temp')
DIFFSDIR = os.path.join(JSONDIR, 'diffs')

import logging
logpath = os.path.join(os.path.dirname(__file__), 'run.log')
logformat = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(
    filename=logpath,
    level=logging.INFO,
    format=logformat
)


# processes for multiprocessing
PROCESSES = 8 

SCALES = {
    'pcs': 1,
    'T': 1000,
    'M': 1000000,
    'MB': 1048576,
    'TB': 1073741824,
}

INTEGERS = {
    's': {
        'Error': 'pcs/s',
        'TxObjects': 'M/s',
        'RxObjects': 'M/s',
        'TxElements': 'TB/s',
        'RxElements': 'TB/s',
        'BBCreditZero': 'M/s',
        'Class3RxFrames': 'M/s',
    },
    'p': {
        'Error': 'pcs/s',
        'TxObjects': 'T/s',
        'RxObjects': 'T/s',
        'TxElements': 'MB/s',
        'RxElements': 'MB/s',
        'BBCreditZero': 'pcs/s',
        'Class3RxFrames': 'T/s',
    }
}

