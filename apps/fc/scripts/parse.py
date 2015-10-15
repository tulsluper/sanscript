#!/usr/bin/env python3

import os
import json
import defs_parsers
from settings import TEXTDIR, JSONDIR, PARSERS
from settings import logging
from defs import dump_data, load_data

def sort_records(records):
    if records and type(records[0]) == dict:
        if 'Switch' in records[0].keys():
            names = load_data(os.path.join(JSONDIR, 'sorted_switchnames.json'), [])
            indexes = {name: num for num, name in enumerate(names)}
            records.sort(key=lambda x: indexes.get(x['Switch'], 0))
    return records


def main():

    commandout = {}
    for filename in os.listdir(TEXTDIR):
        filepath = os.path.join(TEXTDIR, filename)
        system, command = filename.split('.')
        with open(filepath) as f:
            lines = f.readlines()
            for name in PARSERS.get(command, []):
                if not name in commandout:
                    commandout[name] = []
                function = getattr(defs_parsers, 'p_'+name)
                records = function(system, lines)                
                commandout[name] += records
    
    for command, records in commandout.items():
        records = sort_records(records)
        filepath = os.path.join(JSONDIR, command)
        dump_data(filepath, records)
        logging.info('%s | %s records' %(command, len(records)))

    return

if __name__ == '__main__':
    main()
