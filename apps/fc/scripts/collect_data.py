#!/usr/bin/env python3

from run_scripts import run


scripts = [
    'prepare_data_dirs',
    'sort_systems',

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


def main():
    run(scripts)


if __name__ == '__main__':
    main()
