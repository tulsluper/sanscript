#!/usr/bin/env python3

import os
import sys
import json
from settings import JSONDIR
from settings import logging
from defs import load_data, dump_data


def main():

    filepath = os.path.join(JSONDIR, 'name')
    records = load_data(filepath, [])
    online_wwns = []
    for record in records:
        online_wwns.append(record['PortName'])
        online_wwns.append(record['NodeName'])

    filepath = os.path.join(JSONDIR, 'alias')
    records = load_data(filepath, [])
    status_aliases = []
    for record in records:
        wwns = {}
        status = 'Normal'
        for wwn in record['Wwns']:
            if wwn in online_wwns:
                wwns[wwn] = True
            else:
                wwns[wwn] = False
                status = 'Warning'
        status_aliases.append({
            'Fabric': record['Fabric'],
            'Name': record['Name'],
            'Wwns': wwns,
            'Status': status,
        })

    fabaliwwns = {}
    for record in status_aliases:
        fabaliwwns['%s.%s' %(record['Fabric'], record['Name'])] = record['Wwns']

    filepath = os.path.join(JSONDIR, 'zone')
    records = load_data(filepath, [])
    status_zones = []
    for record in records:
        aliases = {}
        status = 'Normal'
        for name in record['Aliases']:
            wwns = fabaliwwns.get('%s.%s' %(record['Fabric'], name), {})
            aliases[name] = wwns
            for wwn in wwns:
                if not wwn in online_wwns:
                    status = 'Warning'
        status_zones.append({
            'Fabric': record['Fabric'],
            'Name': record['Name'],
            'Aliases': aliases,
            'Status': status,
        })

    filepath = os.path.join(JSONDIR, 'alias_status')
    dump_data(filepath, status_aliases)
    logging.info('%s | %s records' %('alias_status', len(status_aliases)))
    filepath = os.path.join(JSONDIR, 'zone_status')
    dump_data(filepath, status_zones)
    logging.info('%s | %s records' %('alias_zones', len(status_zones)))

    return


if __name__ == '__main__':
    main()
