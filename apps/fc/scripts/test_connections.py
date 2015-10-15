#!/usr/bin/env python3

import os
import logging
import time
from defs import run_with_locker, get_logger, load_data, ssh_run

basepath = os.path.realpath(__file__)[:-3]
logfile = basepath + '.log'
lockfile = basepath + '.lock'

@run_with_locker(lockfile)
def run():
    logger = get_logger(logfile, 'sanscript.fc')

    connections = []
    dirpath = os.path.dirname(os.path.realpath(__file__))
    for filename in ['FabricConnection.json', 'SwitchConnection.json']:
        filepath = os.path.join(dirpath, filename)
        connections += load_data(filepath, [])

    for connection in connections:
        args = [connection[key] for key in ['name', 'address', 'username', 'password']]
        args.append([])
        system, outs, errs, exception = ssh_run(args)
        if exception:
            logger.warning('%s test failed - %s' %(system, exception))
        else:
            logger.info('%s test success' %system)

   
if __name__ == '__main__':
    run()
