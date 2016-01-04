#!/usr/bin/env python3

import os
from defs import run_with_locker
from run_scripts import set_logger, run

basepath = os.path.realpath(__file__)[:-3]
lockfile = basepath + '.lock'
logfile = basepath + '.log'


scripts = [
    'run',
    'db_sql',
    'sum_records',
]

@run_with_locker(lockfile)
def main():
    set_logger(logfile)
    run(scripts)



if __name__ == '__main__':
    main()
