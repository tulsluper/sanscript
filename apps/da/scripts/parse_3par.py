#!/usr/bin/env python3

import os
import logging
from settings import TEXTDIR, JSONDIR
from defs import load_data, dump_data

import defs_parsers_3par as defs_parsers
from settings import PARSERS_3PAR as PARSERS
TRIBE = '3par'

def main():

    directory = os.path.join(JSONDIR, TRIBE)
    if not os.path.exists(directory):
        os.makedirs(directory)

    models_filepath = os.path.join(JSONDIR, 'models')
    models = load_data(models_filepath)
    models = models.get(TRIBE, [])

    commandout = {}
    for filename in os.listdir(TEXTDIR):
        filepath = os.path.join(TEXTDIR, filename)
        system, command = filename.split('.')
        if system in models:
            with open(filepath) as f:
                lines = f.readlines()

                for parser_command, parser in PARSERS:
                    if command == parser_command:
                        if not parser in commandout:
                            commandout[parser] = []
                        function = getattr(defs_parsers, 'p_'+parser)
                        records = function(system, lines)                
                        commandout[parser] += records
                        break
    
    for command, records in commandout.items():
        filepath = os.path.join(JSONDIR, TRIBE, command)
        logging.info('%s | %s records' %(command, len(records)))
        dump_data(filepath, records)

    return

if __name__ == '__main__':
    main()
