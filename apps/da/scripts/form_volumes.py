#!/usr/bin/env python3

import os
import logging
from settings import JSONDIR
from defs import load_data, dump_data


def get_tpar_volume_hosts():
    filepath = os.path.join(JSONDIR, '3par/vlun')
    data = load_data(filepath)
    xdict = {}
    for record in data:
        wwn = record['VV_WWN']
        if not wwn in xdict:
            xdict[wwn] = set()
        xdict[wwn].add(record['HostName'])
    for key, val in xdict.items():
        xdict[key] = sorted(val)
    return xdict


def tpar_form_volumes(volume_hosts):
    filepath = os.path.join(JSONDIR, '3par/vv')
    data = load_data(filepath)
    xlist = []
    for record in data:
        volume = {
            'Storage': record['Storage'],
            'Uid': record['VV_WWN'],
            'Name': record['Name'],
            'Size': int(record['VSize_MB'])/1024,
            'Hosts': volume_hosts.get(record['VV_WWN'], []),
        }
        xlist.append(volume)
    return xlist


def get_hds_volume_hosts():
    filepath = os.path.join(JSONDIR, 'hds/hgmap')
    data = load_data(filepath)
    xdict = {}
    for record in data:
        uid = '%s %s' %(record['Storage'], record['LUN'])
        if not uid in xdict:
            xdict[uid] = set()
        xdict[uid].add(record['Group'].split(':')[1])
    for key, val in xdict.items():
        xdict[key] = sorted(val)
    return xdict


def hds_form_volumes(volume_hosts):
    filepath = os.path.join(JSONDIR, 'hds/luref')
    data = load_data(filepath)
    xlist = []
    for record in data:
        uid = '%s %s' %(record['Storage'], record['LU'])
        volume = {
            'Storage': record['Storage'],
            'Uid': record['LU'],
            'Name': '',
            'Size': float(record['Capacity']),
            'Hosts': volume_hosts.get(uid, []),
        }
        xlist.append(volume)
    return xlist


def get_eva_form_volumes():
    filepath = os.path.join(JSONDIR, 'eva/vdisk')
    data = load_data(filepath)
    xlist = []
    for record in data:
        if 'hosts' in record:
            hosts = [host.split('\\')[-1] for host in record['hosts'].split()]
        else:
            hosts = []
        volume = {
            'Storage': record['Storage'],
            'Uid': record['objecthexuid'],
            'Name': record['familyname'],
            'Size': float(record['requestedcapacity']),
            'Hosts': sorted(hosts),
        }
        xlist.append(volume)
    return xlist


def main():
    tpar_volume_hosts = get_tpar_volume_hosts()
    tpar_volumes = tpar_form_volumes(tpar_volume_hosts)
    hds_volume_hosts = get_hds_volume_hosts()
    hds_volumes = hds_form_volumes(hds_volume_hosts)
    eva_volumes = get_eva_form_volumes()
    volumes = tpar_volumes + hds_volumes + eva_volumes
    filepath = os.path.join(JSONDIR, 'volumes')
    dump_data(filepath, volumes)
    

if __name__ == '__main__':
    main()

