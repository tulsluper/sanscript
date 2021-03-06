#!/usr/bin/env python3

import os
from datetime import datetime
from itertools import chain
from multiprocessing import Pool
from pysnmp.entity.rfc3413.oneliner import cmdgen
from defs import load_data, dump_data
from settings import PROCESSES, JSONDIR
from settings import logging


dirpath = os.path.dirname(os.path.realpath(__file__))
connections = load_data(os.path.join(dirpath, 'SwitchConnection.json'), [])

counters = {
    '1.3.6.1.3.94.1.10.1.3': 'connUnitPortType',
    '1.3.6.1.3.94.1.10.1.17': 'connUnitPortName',
}

names =  [x['name'] for x in connections]


def sort_uports(xlist):
    xlist.sort(key=lambda x: (names.index(x[0].split()[0]), int(x[0].split()[1])))
    return xlist


if not os.path.exists(JSONDIR):
    os.makedirs(JSONDIR)


def counter_from_number(number, counters=counters):
    for oid, counter in counters.items():
        if str(number).startswith(oid):
            return counter
    else:
        return None


def snmpwalk(connection, counters=counters):
    """
    perform snmpwalk command and return counters values;
    """
    values = {}
    address = connection['address']
    name = connection['name']
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
        cmdgen.CommunityData('public'),
        cmdgen.UdpTransportTarget((address, 161), timeout=5, retries=5),
        *list(counters.keys())
    )
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
                    counter = counter_from_number(number)
                    port = int(number.asTuple()[-1]) -1
                    value = str(value)
                    values['{} {} {}'.format(name, port, counter)] = value
    return values


def multisnmpwalk(oids, connections, processes):
    """
    run snmpwalk processes and concatenate results;
    """
    pool = Pool(processes=processes)
    values = pool.map(snmpwalk, connections)
    values = dict(chain(*map(dict.items, values)))
    return values


def main():
    """
    main function
    """
    pdata = {}
    udata = multisnmpwalk(counters, connections, PROCESSES)
    for uid, value in udata.items():
        switch, port, counter = uid.split()
        uport = '{} {}'.format(switch, port)
        if not uport in pdata:
            pdata[uport] = {}
        if counter == 'connUnitPortType':
            pdata[uport]['porttype'] = value
        elif counter == 'connUnitPortName':
            pdata[uport]['portname'] = value

    records = []
    for uport, record in pdata.items():
        switch, port = uport.split()
        record['switchname'] = switch
        record['portindex'] = port
        records.append(record)

    names =  [x['name'] for x in connections]
    records.sort(key=lambda x: (names.index(x['switchname']), int(x['portindex'])))

    dump_data(os.path.join(JSONDIR, 'configs'), records)

    """
    for counter, xdict in cdata.items():
        xdict = sort_uports(xdict)
        dump_data(os.path.join(JSONDIR, counter), xdict)
        records.append({'counter': counter, 'values': xdict, 'datetime': str(dt)})
    """

    return


if __name__ == '__main__':
    main()
