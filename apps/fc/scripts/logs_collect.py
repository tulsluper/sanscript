#!/usr/bin/env python3

import os
import logging
from datetime import datetime
from multiprocessing import Pool
from contextlib import closing
from defs import run_with_locker, load_data, ssh_run
from settings import PROCESSES, F_COMMANDS, S_COMMANDS, TEXTDIR, JSONDIR

fields = ['name', 'address', 'username', 'password']
dirpath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(dirpath, 'SwitchConnection.json')

fswitches = load_data(os.path.join(JSONDIR, 'fswitch'), {})
fswitches = [x['Switch'] for x in fswitches]

connections = load_data(filepath, [])

S_CONNECTIONS = [[c[k] for k in fields] for c in connections]
F_CONNECTIONS = [x for x in S_CONNECTIONS if x[0] in fswitches]

logging.getLogger("paramiko").setLevel(logging.WARNING)

def main():

    dtstr = datetime.now().strftime("%Y-%m-%d.%H-%M-%S")

    F_COMMANDS = [
        ['fabriclog', 'fabriclog --show'],
    ]
    S_COMMANDS = [
        ['portlogdump', 'portlogdump'],
    ]

    args1 = [c + [F_COMMANDS] for c in F_CONNECTIONS]
    args2 = [c + [S_COMMANDS] for c in S_CONNECTIONS]
    args = args1 + args2

    with closing(Pool(PROCESSES)) as pool:
        for result in pool.imap_unordered(ssh_run, args):
            system, outs, errs, exception = result
            if not exception:
                for command, out in outs.items():
                    filename = '%s.%s' %(system, command)
                    filepath = os.path.join(TEXTDIR, filename)
                    with open(filepath, 'w') as f:
                        f.write(out)
                        logging.info('%s | %s lines' %(filename, len(out)))
            else:
                logging.warning('%s %s' %(system, exception))

    return


if __name__ == '__main__':
    main()

