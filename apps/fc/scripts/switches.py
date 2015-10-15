#!/usr/bin/env python3

import os
from settings import logging
from settings import JSONDIR
from defs import load_data, dump_data


def main():
    records = []

    filepath = os.path.join(JSONDIR, 'sorted_switchnames')
    sorted_switchnames = load_data(filepath, [])

    filepath = os.path.join(JSONDIR, 'switch')
    swi_records = load_data(filepath, [])

    filepath = os.path.join(JSONDIR, 'serial')
    ser_records = load_data(filepath, [])

    filepath = os.path.join(JSONDIR, 'version')
    ver_records = load_data(filepath, [])

    filepath = os.path.join(JSONDIR, 'fswitch')
    fsw_records = load_data(filepath, [])

    filepath = os.path.join(JSONDIR, 'agswitch')
    ags_records = load_data(filepath, [])

    for swi_record in swi_records:
        switch = swi_record['Switch']
        record = {
            'Switch': swi_record['Switch'],
            'switchType': swi_record['switchType'],
            'switchMode': swi_record['switchMode'],
            'switchRole': swi_record['switchRole'] if 'switchRole' in swi_record else '',
        }
        if record['switchMode'] == 'Access Gateway Mode':
            record['switchMode'] = 'AG'

        for records2 in [fsw_records, ags_records]:
            for record2 in records2:
                if switch == record2['Switch']:
                    record['Fabric'] = record2['Fabric']

        for ser_record in ser_records:
            if switch == ser_record['Switch']:
                record.update({
                    'Part_Num': ser_record['Part_Num'],
                    'Serial_Num': ser_record['Serial_Num'],
                })
        for ver_record in ver_records:
            if switch == ver_record['Switch']:
                record.update({
                    'Fabric_OS': ver_record['Fabric_OS'],
                })
        records.append(record)

    dump_data(os.path.join(JSONDIR, 'switch_common'), records)
    logging.info('%s | %s records' %(__name__, len(records)))

    return

if __name__ == '__main__':
    main()

