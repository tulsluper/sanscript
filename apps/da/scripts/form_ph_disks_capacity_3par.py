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



def pd_types_capacity(data):
    mbfields = ['Size_MB', 'Volume_MB', 'Free_MB', 'Unavail_MB', 'Failed_MB', 'Spare_MB']
    xdict = {}
    for pd in data:
        key = '{} {}'.format(pd['Storage'], pd['Type'])
        if not key in xdict:
            xdict[key] = {field: 0 for field in mbfields}
        for field in mbfields:
            xdict[key][field] += int(pd[field])
    records = []
    for key, record in xdict.items():
        storage, pdtype = key.split()
        record.update({'Storage': storage, 'Type': pdtype})
        records.append(record)
    return records


def main():
    filepath = os.path.join(JSONDIR, '3par/showpd')
    data = load_data(filepath)
    records = pd_types_capacity(data)

    sorted_systems = load_data(os.path.join(JSONDIR, 'sorted_systems'), [])
    records = sort_storage_records(records, sorted_systems)

    filepath = os.path.join(JSONDIR, '3par/pd_capacity')
    dump_data(filepath, records)


if __name__ == '__main__':
    main()

