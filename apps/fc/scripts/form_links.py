#!/usr/bin/env python3

import os
import sys
import json
from settings import JSONDIR, TEXTDIR
from settings import logging
from defs import load_data, dump_data

fields = ['name', 'address', 'username', 'password']
dirpath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(dirpath, 'SwitchConnection.json')
connections = load_data(filepath, [])
CONNECTIONS = [[c[k] for k in fields] for c in connections]


def get_domains():
    domains = {}
    filepath = os.path.join(JSONDIR, 'switch')
    records = load_data(filepath, [])
    for record in records:
        domain = record.get('switchDomain')
        if domain:
            domains[domain] = record['Switch']
    return domains


def get_speeds():
    speeds = {}
    filepath = os.path.join(JSONDIR, 'port')
    records = load_data(filepath, [])
    for record in records:
        key = '%s.%s' %(record['Switch'], record['Index'])
        value = record['Speed'].replace('G','').replace('N','')
        speeds[key] = value
    return speeds


def get_addresses():
    addresses = {}
    filepath = os.path.join(JSONDIR, 'port')
    records = load_data(filepath, [])
    for record in records:
        key = '%s.%s' %(record['Switch'], record['Index'])
        value = record['Address']
        addresses[key] = value
    return addresses


def get_n_trunk_ports():
    n_trunk_ports = {}
    filepath = os.path.join(JSONDIR, 'port')
    records = load_data(filepath, [])
    for record in records:
        if record['Type'] == 'N-Port' and 'Trunk' in record['Comment']:
            n_trunk_ports[record['Comment'][2:8]] = record
    return n_trunk_ports


def get_n_link_ports():
    n_link_ports_list = []
    filepath = os.path.join(JSONDIR, 'port')
    records = load_data(filepath, [])
    for record in records:
        if record['Type'] == 'N-Port' and not 'Trunk' in record['Comment']:
            n_link_ports_list.append(record)
    return n_link_ports_list


def get_f_link_ports():
    f_link_ports = {}
    filepath = os.path.join(JSONDIR, 'port')
    records = load_data(filepath, [])
    for record in records:
        if record['Type'] == 'F-Port':
            f_link_ports[record['Address']] = record
    return f_link_ports



domains = get_domains()
speeds = get_speeds()
addresses = get_addresses()
n_trunk_ports = get_n_trunk_ports()
n_link_ports_list = get_n_link_ports()
f_link_ports = get_f_link_ports()


def f_etrunk():
    records = []
    for filename in os.listdir(TEXTDIR):
        sw1, command = filename.split('.')
        if command == 'trunkshow':
            filepath = os.path.join(TEXTDIR, filename)
            with open(filepath) as f:
                lines = f.readlines()
                prevTrunkId = None
                for line in lines:
                    if line != '\n' and not 'Error:' in line:
                        TrunkId = line[:3].strip()
                        port1 = line[4:7].strip()
                        port2 = line[9:12].strip()
                        sw2 = line[36:40].strip()
                        Master = True if len(line) > 52 else False
            
                        if TrunkId == '':
                            TrunkId = prevTrunkId
                        else:
                            prevTrunkId = TrunkId

                        sw2 = domains.get(sw2, sw2)
                        Speed = speeds.get('%s.%s' %(sw1, port1), 0)
                        reverse_flag = True

                        # chech if record is reverse
                        sw_list = [c[0] for c in CONNECTIONS]
                        sw_index1 = sw_list.index(sw1) if sw1 in sw_list else len(sw_list)
                        sw_index2 = sw_list.index(sw2) if sw2 in sw_list else len(sw_list)
                        if sw_index1 > sw_index2:
                            reverse_flag = True
                        else:
                            reverse_flag = False

                        record = {
                            'Switch1': sw1,
                            'Port1': int(port1),
                            'Switch2': sw2,
                            'Port2': int(port2),
                            'Speed': int(Speed),
                            'TrunkId': int(TrunkId) if TrunkId else None,
                            'Master': Master,
                            'E_Trunk': True,
                            'F_Trunk': None,
                            'F_Link': None,
                            'Reverse': reverse_flag
                        }
                        records.append(record)
                        if sw2.isdigit():
                            record = {
                                'Switch1': sw2,
                                'Port1': int(port2),
                                'Switch2': sw1,
                                'Port2': int(port1),
                                'Speed': int(Speed),
                                'TrunkId': None,
                                'Master': Master,
                                'E_Trunk': True,
                                'F_Trunk': None,
                                'F_Link': None,
                                'Reverse': True
                            }
                            records.append(record)
    return records


def f_ftrunk():
    records = []
    ad_pta = {}
    for filename in os.listdir(TEXTDIR):
        sw1, command = filename.split('.')
        if command == 'porttrunkarea':
            filepath = os.path.join(TEXTDIR, filename)
            with open(filepath) as f:
                lines = f.readlines()
                for line in lines:
                    if line != '\n' and not 'Error:' in line:
                        if '->' in line:
                            items = line.split()
                            if items[0] == 'Trunk':
                                TrunkId = items[2][:-1]
                                plid = 3
                                Master = True
                            else:
                                plid = 0
                                Master = False
                            port1, port2 = items[plid].split('->')
                            Address = addresses.get('%s.%s' %(sw1, TrunkId), 0)
                            port2record = n_trunk_ports.get(Address, {})
                            sw2 = port2record.get('Switch', '')
                            speed = port2record.get('Speed', '').replace('G','').replace('N','').replace('A','')
                            record_direct = {
                                'Switch1': sw1,
                                'Port1': int(port1),
                                'Switch2': sw2,
                                'Port2': int(port2),
                                'Speed': speed,
                                'TrunkId': int(TrunkId),
                                'Master': Master,
                                'E_Trunk': None,
                                'F_Trunk': True,
                                'F_Link': None,
                                'Reverse': False #direct
                            }
                            record_reverse = {
                                'Switch1': sw2,
                                'Port1': int(port2),
                                'Switch2': sw1,
                                'Port2': int(port1),
                                'Speed': speed,
                                'TrunkId': int(port2record.get('Port')) if port2record.get('Port') else None,
                                'Master': Master,
                                'E_Trunk': None,
                                'F_Trunk': True,
                                'F_Link': None,
                                'Reverse': True, #reverse
                            }
                            records.append(record_direct)
                            records.append(record_reverse)
    return records


def form_f_links():
    records = []
    for port1 in n_link_ports_list:
        port2_Address = port1['Comment'][2:8]
        port2 = f_link_ports.get(port2_Address, {})
        record_direct = {
            'Switch1': port1['Switch'],
            'Port1': int(port1['Index']),
            'Switch2': port2['Switch'],
            'Port2': int(port2['Index']),
            'Speed': port1['Speed'].replace('G','').replace('N','').replace('A',''),
            'TrunkId': None,
            'Master': None,
            'E_Trunk': None,
            'F_Trunk': None,
            'F_Link': True,
            'Reverse': False
        }
        record_reverse = {
            'Switch1': port2['Switch'],
            'Port1': int(port2['Index']),
            'Switch2': port1['Switch'],
            'Port2': int(port1['Index']),
            'Speed': port2['Speed'].replace('G','').replace('N','').replace('A',''),
            'TrunkId': None,
            'Master': None,
            'E_Trunk': None,
            'F_Trunk': None,
            'F_Link': True,
            'Reverse': True
        }
        records.append(record_direct)
        records.append(record_reverse)
    return records



def main():
    records = f_etrunk() + f_ftrunk() + form_f_links()
    filepath = os.path.join(JSONDIR, 'link')
    dump_data(filepath, records)
    logging.info('%s | %s records' %('link', len(records)))


if __name__ == '__main__':
    main()


