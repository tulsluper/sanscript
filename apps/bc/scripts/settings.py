"""
"""
import os

APPNAME = 'bc'
BASEDIR = os.path.join(os.path.dirname(__file__), '../../../')
JSONDIR = os.path.join(BASEDIR, 'data/{}/json/'.format(APPNAME))

TEMPFILE = os.path.join(JSONDIR, 'temp')
DIFFSDIR = os.path.join(JSONDIR, 'diffs')


# processes for multiprocessing
PROCESSES = 4

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

