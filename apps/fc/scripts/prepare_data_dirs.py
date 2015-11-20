#!/usr/bin/env python3

import os
import logging
import settings


def main():
    for name in ['TEXTDIR', 'JSONDIR', 'TEMPDIR']:
        directory = getattr(settings, name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        logging.info('{} = {}'.format(name, os.path.realpath(directory)))
    return


if __name__ == '__main__':
    main()
