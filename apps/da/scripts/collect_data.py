#!/usr/bin/env python3

from run_scripts import run


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
    'form_capacity_3par',
    'form_capacity',

    'save_into_db',
    'save_app_info',
]


def main():
    run(scripts)


if __name__ == '__main__':
    main()
