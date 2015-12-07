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
    'clean_old_files',

    'collect',
    'collect_ports',
    'parse',
    'form_status',
    'form_links',
    'build_graph',
    'build_relations',
    'build_paths',
    'switches',
    'ports',

    'save_into_db',
    'save_app_info',
]


@run_with_locker(lockfile)
def main():
    set_logger(logfile)
    run(scripts)


if __name__ == '__main__':
    main()
