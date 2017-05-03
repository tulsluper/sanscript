#!/usr/bin/env python3

import os
from settings import JSONDIR, logging
from defs import load_data, dump_data


def sort_storage_records(records, sorted_systems):
    try:
        records.sort(key=lambda x: sorted_systems.index(x['Storage']))
    except:
        pass
    return records

def pd_types_quantity(data):
    mbfields = ['Size_MB', 'Volume_MB', 'Free_MB', 'Unavail_MB', 'Failed_MB', 'Spare_MB']
    fields = ['Storage', 'Type', 'MediaType', 'Capacity', 'RPM']
    xdict = {}
    for pd in data:
        key = ' '.join([pd[f] for f in fields])
        if not key in xdict:
            xdict[key] = 0
        xdict[key] += 1
    records = []
    for key, number in xdict.items():
        record = dict(zip(fields, key.split()))
        record.update({'Number': number})
        records.append(record)
    return records


def main():
    filepath = os.path.join(JSONDIR, '3par/showpd')
    data = load_data(filepath)
    records = pd_types_quantity(data)

    sorted_systems = load_data(os.path.join(JSONDIR, 'sorted_systems'), [])
    records = sort_storage_records(records, sorted_systems)

    filepath = os.path.join(JSONDIR, '3par/pd_quantity')
    dump_data(filepath, records)


if __name__ == '__main__':
    main()

