#!/usr/bin/env python3

import os
from defs import run_with_locker
from run_scripts import set_logger, run

basepath = os.path.realpath(__file__)[:-3]
lockfile = basepath + '.lock'
logfile = basepath + '.log'

scripts = [
    'prepare_data_dirs',
    'sort_systems',

    'form_models',
    'collect_3par',
    'collect_eva',
    'collect_hds',
    'parse_3par',
    'parse_eva',
    'parse_hds',
    'form_volumes',
    'form_hosts',
    'form_hosts_capacity',
    'form_capacity_3par',
    'form_capacity',

    'save_into_db',
    'save_app_info',

    'configs_collect', 
    'configs_compare',
    'configs_changes_save',
]


@run_with_locker(lockfile)
def main():
    set_logger(logfile)
    run(scripts)


if __name__ == '__main__':
    main()
