#!/usr/bin/env python3

import os
import logging
from settings import TEXTDIR, JSONDIR
from defs import load_data, dump_data

dirpath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(dirpath, 'StorageConnection.json')
CONNECTIONS = load_data(filepath, [])


def main():
    models = {}
    for connection in CONNECTIONS:
        model = connection['model'].lower()
        name = connection['name']
        if not model in models:
            models[model] = []
        models[model].append(name)

    filepath = os.path.join(JSONDIR, 'models')
    logging.info(models)
    dump_data(filepath, models)

    return


if __name__ == '__main__':
    main()
