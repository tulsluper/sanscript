#!/usr/bin/env python3

import os
import logging
from settings import JSONDIR
from defs import load_data, dump_data


def tpar_form_hosts():
    filepath = os.path.join(JSONDIR, '3par/host')
    data = load_data(filepath, [])
    xdict = {}
    for record in data:
        Storage_Host = '%s %s' %(record['Storage'], record['Name'])
        if not Storage_Host in xdict:
            xdict[Storage_Host] = {
                'Storage': record['Storage'],
                'Host': record['Name'],
                'OS': record['Persona'],
                'WWNs': [],
            }
        wwn = record['WWN_or_Name'].lower()
        wwn = ':'.join([wwn[i:i+2] for i in range(0, len(wwn), 2)])
        if not wwn in xdict[Storage_Host]['WWNs']:
            xdict[Storage_Host]['WWNs'].append(wwn)
    xlist = list(xdict.values())
    logging.info('{} {}'.format('3par', len(xlist)))
    return xlist


def hds_form_hosts():
    filepath = os.path.join(JSONDIR, 'hds/hgwwn')
    data = load_data(filepath, [])
    xdict = {}
    for record in data:
        Storage_Host = '%s %s' %(record['Storage'], record['Host_Group'])
        if not Storage_Host in xdict:
            xdict[Storage_Host] = {
                'Storage': record['Storage'],
                'Host': record['Host_Group'].split(':')[1],
                'OS': '',
                'WWNs': [],
            }
        wwn = record['Port_Name'].lower()
        wwn = ':'.join([wwn[i:i+2] for i in range(0, len(wwn), 2)])
        if not wwn in xdict[Storage_Host]['WWNs']:
            xdict[Storage_Host]['WWNs'].append(wwn)
    xlist = list(xdict.values())
    logging.info('{} {}'.format('hds', len(xlist)))
    return xlist


def eva_form_hosts():
    filepath = os.path.join(JSONDIR, 'eva/host')
    data = load_data(filepath, [])
    xlist = []
    for record in data:
        wwns = []
        for wwn in record['WWNs'].split():
            wwn = wwn.lower().replace('-', '')
            wwn = ':'.join([wwn[i:i+2] for i in range(0, len(wwn), 2)])
            wwns.append(wwn)
        host = {
            'Storage': record['Storage'],
            'Host': record['hostname'],
            'OS': record['osmode'],
            'WWNs': sorted(wwns),
        }
        xlist.append(host)

    logging.info('{} {}'.format('eva', len(xlist)))
    return xlist


def main():
    tpar_form_hosts()
    hds_form_hosts()
    eva_form_hosts()
    hosts = tpar_form_hosts() + hds_form_hosts() + eva_form_hosts()
    filepath = os.path.join(JSONDIR, 'hosts')
    dump_data(filepath, hosts)
    

if __name__ == '__main__':
    main()

