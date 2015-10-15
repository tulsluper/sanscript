#!/usr/bin/env python3

import os
import logging
from settings import JSONDIR, CONNECTIONS
from defs import load_data, dump_data


def main():
    connections = load_data(CONNECTIONS, [])
    names = [c['name'] for c in connections]
    dump_data(os.path.join(JSONDIR, 'sorted_systems'), names)
    logging.info(str(names))
    return


if __name__ == '__main__':
    main()
