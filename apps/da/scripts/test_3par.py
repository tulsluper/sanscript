#!/usr/bin/env python3

import os
from defs import load_data, ssh_run
from settings import logging

logging.getLogger("paramiko").setLevel(logging.WARNING)

dirpath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(dirpath, 'StorageConnection.json')
CONNECTIONS = load_data(filepath, [])


def main():
    for connection in CONNECTIONS:
        if connection['model'] == '3PAR':
            args = [connection[key] for key in ['name', 'address', 'username', 'password']]
            args.append([])
            systemname, outs, errs, exception = ssh_run(args)
            if exception:
                logging.warning('%s test failed - %s' %(systemname, exception))
            else:
                logging.info('%s test success' %systemname)
    return


if __name__ == '__main__':
    main()
