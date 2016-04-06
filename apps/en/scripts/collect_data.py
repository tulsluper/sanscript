#!/usr/bin/env python3

import os
import importlib
import logging
from defs import run_with_locker

basepath = os.path.realpath(__file__)[:-3]

lockfile = basepath + '.lock'

logfile = basepath + '.log'
open(logfile, 'w').close()

logFormatter = logging.Formatter(
    '%(asctime)s %(module)s %(levelname)s %(message)s',
    '%Y-%m-%d %H:%M:%S'
)
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler(logfile)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

rootLogger.setLevel(logging.INFO)


scripts = [
    'collect',
    'parse',
    'parse2',
    'save_into_db',
    'save_app_info',
]

@run_with_locker(lockfile)
def main():
    logging.info('# START')
    for script_name in scripts:
        logging.info('# START {}'.format(script_name))
        script = importlib.import_module(script_name)
        script.main()
        logging.info('# FINISH {}'.format(script_name))
    logging.info('# FINISH') 
    return


if __name__ == '__main__':
    main()
