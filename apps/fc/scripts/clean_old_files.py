#!/usr/bin/env python3

import os
import logging
from settings import TEXTDIR, CONNECTIONS
from defs import load_data, dump_data


def main():
    connections = load_data(CONNECTIONS, [])
    names = [c['name'] for c in connections]
    for filename in os.listdir(TEXTDIR):
        if '.' in filename:
            systemname = filename.split('.')[0]
            if not systemname in names:
                filepath = os.path.join(TEXTDIR, filename)
                os.remove(filepath)
                logging.info('removed: {}'.format(filepath))
    return


if __name__ == '__main__':
    main()
