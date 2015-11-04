#!/usr/bin/env python3

import os
import logging
from settings import JSONDIR
from defs import load_data, dump_data


def main():
    
    storhosts = {}
    volumes = load_data(os.path.join(JSONDIR, 'volumes'), [])
    for volume in volumes:
        uid = '+'.join([volume['Storage'], ' '.join(sorted(volume['Hosts']))])
        if not uid in storhosts:
            storhosts[uid] = 0
        storhosts[uid] += float(volume['Size'])

    records = []
    for uid, size in storhosts.items():
        storage, hosts_str = uid.split('+')
        hosts = hosts_str.split()
        record = {
            'Storage': storage,
            'Hosts': hosts,
            'Size': size,
        }
        records.append(record)
    dump_data(os.path.join(JSONDIR, 'hosts_capacity'), records)

if __name__ == '__main__':
    main()

