#!/usr/bin/env python3

import importlib
import logging


def set_logger(logfile):
    open(logfile, 'w').close()
    logFormatter = logging.Formatter(
        '%(asctime)s %(module)s %(levelname)s %(message)s',
        '%Y-%m-%d %H:%M:%S')
    rootLogger = logging.getLogger()
    fileHandler = logging.FileHandler(logfile)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    rootLogger.setLevel(logging.INFO)
    return


def run(scripts):
    logging.info('# START')
    for script_name in scripts:
        logging.info('# START {}'.format(script_name))
        script = importlib.import_module(script_name)
        script.main()
        logging.info('# FINISH {}'.format(script_name))
    logging.info('# FINISH') 
    return
