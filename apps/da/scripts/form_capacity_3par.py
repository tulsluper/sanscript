#!/usr/bin/env python3

import os
from settings import JSONDIR, logging
from defs import load_data, dump_data


def main():

    records = []

    filepath = os.path.join(JSONDIR, '3par/sys')
    sys_data = load_data(filepath)
    raw_total_sizes = {r["Storage"]: int(r["TotalCap"]) for r in sys_data}
    raw_alloc_sizes = {r["Storage"]: int(r["AllocCap"]) for r in sys_data}

    filepath = os.path.join(JSONDIR, '3par/vv')
    data = load_data(filepath)

    sizes = {}

    for record in data:
        storage = record['Storage']
        if not storage in sizes:
            sizes[storage] = {
                'full': 0, 'cpvv': 0, 'tpvv': 0, 'snp': 0,
                'tpvv_used': 0, 'tpvv_free': 0,
                'copy': 0
            }
        prov = record['Prov']
        size = int(record['VSize_MB'])
        used_size = int(record['Usr_Used_MB']) if record['Usr_Used_MB'] != '--' else 0
        copy_size = int(record['VSize_MB']) if record['SnpCPG'] != '--' and record['UsrCPG'] != '--' else 0
        sizes[storage][prov] += size
        sizes[storage]['tpvv_used'] += used_size if prov == 'tpvv' else 0
        sizes[storage]['copy'] += copy_size

    for storage, stordict in sizes.items():
        raw_total = raw_total_sizes.get(storage)
        raw_alloc = raw_alloc_sizes.get(storage)

        TOTAL = raw_total/2*0.95
        RESERVE = raw_total/2*0.05

        USED = stordict['full'] + stordict['cpvv'] + stordict['tpvv'] + stordict['copy']
        FREE = TOTAL - USED

        REAL = stordict['full'] + stordict['cpvv'] + stordict['tpvv_used']
        reserve_used = raw_alloc/2 - REAL
        
        reserve_overused = 0
        if RESERVE > reserve_used:
            reserve_free = RESERVE - reserve_used
        else:
            reserve_overused = reserve_used - RESERVE
            reserve_free = 0
            FREE = FREE - reserve_overused

        OVERPROVISIONED = 0
        if FREE < 0:
            OVERPROVISIONED = -FREE
            USED += FREE
            FREE = 0

        sizes[storage]['TOTAL'] = TOTAL
        sizes[storage]['USED'] = USED
        sizes[storage]['FREE'] = FREE
        sizes[storage]['OVERPROVISIONED'] = OVERPROVISIONED
        sizes[storage]['RESERVE'] = RESERVE
        sizes[storage]['RESERVE_OVERUSED'] = reserve_overused
        sizes[storage]['tpvv_free'] = stordict['tpvv'] - stordict['tpvv_used']
        sizes[storage]['reserve_used'] = reserve_used
        sizes[storage]['reserve_free'] = reserve_free
 
        record = {k: round(v/1024.0/1024, 2) for k, v in stordict.items()}
        record['Storage'] = storage
        records.append(record)

        logging.info(storage)


    filepath = os.path.join(JSONDIR, 'capacity_3par')
    dump_data(filepath, records)


if __name__ == '__main__':
    main()

