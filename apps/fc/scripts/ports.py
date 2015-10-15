#!/usr/bin/env python3

import os
from settings import logging
from settings import JSONDIR
from defs import load_data, dump_data


def main():
    records = []

    filepath = os.path.join(JSONDIR, 'port')
    records0 = load_data(filepath, [])

    filepath = os.path.join(JSONDIR, 'portshow')
    records1 = load_data(filepath, [])

    filepath = os.path.join(JSONDIR, 'swport_alias')
    records2 = load_data(filepath, [])

    for record0 in records0:
        switch = record0['Switch']
        uPort = record0['uPort']
        Index = record0['Index']

        record = {}
        for key in ['Switch', 'uPort', 'Index', 'Speed', 'State', 'Type']:
            record[key] = record0[key]
        for record1 in records1:
            if switch == record1['Switch'] and uPort == record1['uPort']:
                record['portWwn_of_devices_connected'] = record1['portWwn_of_devices_connected']
                record['portName'] = record1['portName']
        for record2 in records2:
            if record2['Swport'] == '%s %s' %(switch, Index):
                record['Aliases'] = record2['Aliases']

        records.append(record)

    dump_data(os.path.join(JSONDIR, 'port_common'), records)
    logging.info('%s | %s records' %('path', len(records)))

    return

if __name__ == '__main__':
    main()

