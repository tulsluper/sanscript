#!/usr/bin/env python3

import os
import json
from datetime import datetime
from time import time
from itertools import chain, product
from multiprocessing import Pool
from pysnmp.entity.rfc3413.oneliner import cmdgen
from defs import load_data, dump_data
from settings import PROCESSES, TEMPFILE, DIFFSDIR

import logging
logpath = os.path.join(os.path.dirname(__file__), 'run.log')
logformat = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(
    filename=logpath,
    level=logging.INFO,
    format=logformat
)


dirpath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(dirpath, 'SwitchConnection.json')
connections = load_data(filepath, [])
filepath = os.path.join(dirpath, 'CounterOid.json')
counters = load_data(filepath, [])
counters = {c["number"]: c["name"] for c in counters}

if not os.path.exists(DIFFSDIR):
    os.makedirs(DIFFSDIR)


def snmpwalk(connection, counters=counters):
    """
    perform snmpwalk command and return counters values;
    """
    values = {}
    address = connection['address']
    name = connection['name']
    cmdGen = cmdgen.CommandGenerator()

    try:
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
            cmdgen.CommunityData('public'),
            # default: UdpTransportTarget(transportAddr, timeout=1, retries=5, tagList=b'')
            cmdgen.UdpTransportTarget((address, 161), timeout=5, retries=5),
            *list(counters.keys())
        )
    except:
        return values

    if errorIndication:
        logging.warning(name)
        logging.warning(errorIndication)
    else:
        if errorStatus:
            logging.warning(name)
            logging.warning('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                )
            )
        else:
            for varBindTableRow in varBindTable:
                for number, value in varBindTableRow:
                    numberitems = number.asTuple()
                    number = '.'.join(map(str, numberitems[:10]))
                    port = int(numberitems[-1])-1
                    counter = counters[number]
                    value = value.prettyPrint()
                    value = int(value.replace(' ', ''), 16)
                    values['%s %s %s' %(name, port, counter)] = value
    return values


def multisnmpwalk(oids, connections, processes):
    """
    run snmpwalk processes and concatenate results;
    """
    pool = Pool(processes=processes)
    values = pool.map(snmpwalk, connections)
    values = dict(chain(*map(dict.items, values)))
    return time(), values


def diffcalc(snmp_values, temp_values):
    """
    calculate differences between snmp values and temp values;
    """
    udiffs = {}
    for key, snmpvalue in snmp_values.items():
        tempvalue = temp_values.get(key, None)
        if tempvalue is not None:
            counter = key.split()[2]
            diff = snmpvalue - tempvalue
        else:
            diff = -1 # error code 1
        if diff:
            udiffs[key] = diff
    return udiffs


def do_temp(snmp_values):
    """
    read data from temp file and rewrite new data;
    """
    filepath = TEMPFILE
    temp_dt = os.path.getmtime(filepath) if os.path.exists(filepath) else None
    temp_values = load_data(filepath, {})
    dump_data(filepath, snmp_values)
    return temp_dt, temp_values


def safe_diffs(udiffs, snmp_dt, temp_dt):
    """
    save diffs;
    """
    diffsdirpath = DIFFSDIR
    delta = int(snmp_dt - temp_dt)
    dt1 = datetime.fromtimestamp(temp_dt).strftime('%Y-%m-%d.%H-%M-%S')
    dt2 = datetime.fromtimestamp(snmp_dt).strftime('%Y-%m-%d.%H-%M-%S')
    dt1date, dt1time = dt1.split('.')
    dt2date, dt2time = dt2.split('.')
    diffsdirpath = os.path.join(diffsdirpath, dt1date)
    if not os.path.exists(diffsdirpath):
        os.makedirs(diffsdirpath)
    filename = '{}.{}.{}'.format(dt1time, dt2time, delta)
    filepath = os.path.join(diffsdirpath, filename)
    with open(filepath, 'w') as f:
        json.dump(udiffs, f)
    return



def main():
    """
    main function
    """
    snmp_dt, snmp_values = multisnmpwalk(counters, connections, PROCESSES)
    temp_dt, temp_values = do_temp(snmp_values)
    if temp_dt:
        udiffs = diffcalc(snmp_values, temp_values)
        safe_diffs(udiffs, snmp_dt, temp_dt)
    return


if __name__ == '__main__':
    main()
