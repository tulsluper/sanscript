#!/usr/bin/env python3

import os
from settings import logging
from settings import JSONDIR
from defs import load_data, dump_data


def main():
    dirpath = os.path.dirname(os.path.realpath(__file__))
    connections = load_data(os.path.join(dirpath, 'SwitchConnection.json'), [])
    names = [c['name'] for c in connections]
    dump_data(os.path.join(JSONDIR, 'sorted_switchnames.json'), names)
    return


if __name__ == '__main__':
    main()
