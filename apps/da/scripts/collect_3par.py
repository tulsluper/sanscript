#!/usr/bin/env python3

import os
from defs import load_data, ssh_run
from settings import logging
from settings import TEXTDIR
from settings import COMMANDS_3PAR as COMMANDS

logging.getLogger("paramiko").setLevel(logging.WARNING)

dirpath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(dirpath, 'StorageConnection.json')
CONNECTIONS = load_data(filepath, [])


def main():
    for connection in CONNECTIONS:
        if connection['model'] == '3PAR':
            args = [connection[key] for key in ['name', 'address', 'username', 'password']]
            args = args + [COMMANDS]
            systemname, outs, errs, exception = ssh_run(args)
    
            if exception:
                logging.warning('%s - %s' %(systemname, exception))
            for commandname, out in outs.items():
                filename = '%s.%s' %(systemname, commandname)
                filepath = os.path.join(TEXTDIR, filename)
                with open(filepath, 'w') as f:
                    f.write(out)
                    logging.info('%s | %s lines' %(
                        filename, len(out.strip().split('\n'))))
    return


if __name__ == '__main__':
    main()
