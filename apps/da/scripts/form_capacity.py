#!/usr/bin/env python3

import os
from settings import JSONDIR, logging
from defs import load_data, dump_data


def sum_3par():
    capD = {}
    filepath = os.path.join(JSONDIR, '3par', 'sys')
    data = load_data(filepath)
    for record in data:
        xdict = {
            'RawTotal': record['TotalCap'],
            'RawData': record['TotalCap'],
            'RawSpare': 0,
            'RawAllocated': record['AllocCap'],
            'RawFree': record['FreeCap'],
        }
        for key, val in xdict.items():
            xdict[key] = float(val)/1024/1024
        capD[record['Storage']] = xdict
      
    return capD
     

def sum_eva():
    capD = {}
    filepath = os.path.join(JSONDIR, 'eva', 'system')
    data = load_data(filepath)
    for record in data:
        xdict = {
            'RawTotal': record['totalstoragespace'],
            'RawData': record['totalstoragespace'],
            'RawSpare': 0,
            'RawAllocated': record['usedstoragespace'],
            'RawFree': float(record['totalstoragespace']) - float(record['usedstoragespace']),
            'FormattedAvailable': (float(record['totalstoragespace']) - float(record['usedstoragespace']))/2
        }
        for key, val in xdict.items():
            xdict[key] = float(val)/1024
        capD[record['Storage']] = xdict
    return capD


def sum_hds():
    capD = {}
    filepath = os.path.join(JSONDIR, 'hds', 'drive_status')
    data = load_data(filepath)
    filepath = os.path.join(JSONDIR, 'hds', 'drive_vendor')
    data2 = load_data(filepath)
    for record in data:
        for record2 in data2:
            if record['Storage'] == record2['Storage'] and record['HDU'] == record2['HDU']:
                record.update(record2)
    for record in data:
        storage = record['Storage']
        #0.9313 = 1000*1000*1000/1024/1024/1024/1000
        drive_size = int(record['Capacity'].replace('GB', ''))*0.9313/1024
        Type = record['Type']
        Status = record['Status']
        if not storage in capD:
            capD[storage] = {'RawTotal': 0, 'RawData': 0, 'RawSpare': 0, 'RawAllocated': 0, 'RawFree': 0}
        capD[storage]['RawTotal'] += drive_size
        if Type == 'Data':
            capD[storage]['RawData'] += drive_size
        if Type == 'Spare' and Status == 'Standby':
            capD[storage]['RawSpare'] += drive_size

    return capD


def sum_form_cap():
    filepath = os.path.join(JSONDIR, 'volumes')
    data = load_data(filepath)
    xdict = {}
    for record in data:
        storage = record['Storage']
        size = record['Size']
        if not storage in xdict:
            xdict[storage] = {
                'FormattedTotal': 0,
                'FormattedUsed': 0,
                'FormattedPresented': 0,
                'FormattedNotPresented': 0,
                'FormattedAvailable': 0,
            }
        xdict[storage]['FormattedUsed'] += size
        if record['Hosts']:
            xdict[storage]['FormattedPresented'] += size
        else:
            xdict[storage]['FormattedNotPresented'] += size
    for storage, size in xdict.items():
        xdict[storage]['FormattedUsed'] = round(size['FormattedUsed']/1024, 2)
        xdict[storage]['FormattedPresented'] = round(size['FormattedPresented']/1024, 2)
        xdict[storage]['FormattedNotPresented'] = round(size['FormattedNotPresented']/1024, 2)
    return xdict


def sum_form_3par_avail():
    filepath = os.path.join(JSONDIR, 'capacity_3par')
    data = load_data(filepath)
    xdict = {}
    for record in data:
        xdict[record['Storage']] = {
            'FormattedAvailable': record['FREE'],
        }
    return xdict


def sum_form_hds_cap():
    filepath = os.path.join(JSONDIR, 'hds/dppool')
    data1 = load_data(filepath)
    filepath = os.path.join(JSONDIR, 'hds/rgref')
    data2 = load_data(filepath)
    xdict = {}
    for record in data1:
        storage = record['Storage']
        if not storage in xdict:
            xdict[storage] = {'FormattedAvailable': 0}
        FREE = float(record['Total_Capacity']) - float(record['Consumed_Capacity'])
        xdict[storage]['FormattedAvailable'] += FREE
    for record in data2:
        storage = record['Storage']
        if not storage in xdict:
            xdict[storage] = {'FormattedAvailable': 0}
        FREE = float(record['Free_Capacity'])
        xdict[storage]['FormattedAvailable'] += FREE
    for storage, stordict in xdict.items():
        for key, val in stordict.items():
            xdict[storage][key] = float(val)/1024
    return xdict


def main():
    filepath = os.path.join(JSONDIR, 'models')
    models = load_data(filepath)

    RawCapD = {}
    RawCapD.update(sum_3par())
    RawCapD.update(sum_eva())
    RawCapD.update(sum_hds())
    FormCapD = sum_form_cap()
    Form3parAvailD = sum_form_3par_avail()
    FormHdsAvailD = sum_form_hds_cap()
    records = []
    for storage in RawCapD:
        record = {'Storage': storage}
        record.update(RawCapD[storage])
        record.update(FormCapD[storage])
        record.update(Form3parAvailD.get(storage, {}))
        record.update(FormHdsAvailD.get(storage, {}))
        if storage in models.get('eva', []):
            record['FormattedAvailable'] = record['RawFree']/2
        elif storage in models.get('hds', []):
            rate = record['RawData']/(record['FormattedUsed'] + record['FormattedAvailable'])
            record['RawAllocated'] = record['FormattedUsed']*rate
            record['RawFree'] = record['FormattedAvailable']*rate
        record['FormattedTotal'] = record['FormattedUsed'] + record['FormattedAvailable']
        records.append(record)
    filepath = os.path.join(JSONDIR, 'capacity')
    dump_data(filepath, records)
    return


if __name__ == '__main__':
    main()
