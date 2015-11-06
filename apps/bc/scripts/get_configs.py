#!/usr/bin/env python3

import os
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
    '1.3.6.1.3.94.1.10.1.17': 'connUnitPortName'
}


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
                    print(dir(value))
                    value = str(value)
                    values['%s %s %s' %(name, port, counter)] = value
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
    data = multisnmpwalk(counters, connections, PROCESSES)
    dump_data(os.path.join(JSONDIR, 'configs'), data)
    return


if __name__ == '__main__':
    main()
