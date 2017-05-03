#!/usr/bin/env python3

import os
import logging
from settings import JSONDIR, CONFIGSDIR
from defs import load_data, dump_data


def main():
    notedata = load_data(os.path.join(CONFIGSDIR, 'note.json'), {})
    if notedata and type(notedata) == dict:
        note = list(notedata.values())[0]
    else:
        note = '?'
    records = load_data(os.path.join(JSONDIR, 'changes'), {})
    for record in records:
        record['Note'] = note
    dump_data(os.path.join(JSONDIR, 'changes'), records)
    logging.info('Note: %s' %note)
    return


if __name__ == '__main__':
    main()
