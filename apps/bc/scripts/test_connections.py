#!/usr/bin/env python3

import os
from defs import run_with_locker, get_logger, load_data
from pysnmp.entity.rfc3413.oneliner import cmdgen


basepath = os.path.realpath(__file__)[:-3]
logfile = basepath + '.log'
lockfile = basepath + '.lock'


@run_with_locker(lockfile)
def run():
    logger = get_logger(logfile, 'sanscript.fc')
    logger.info('START')

    dirpath = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dirpath, 'SwitchConnection.json')
    connections = load_data(filepath, [])

    for connection in connections:
        systemname = connection['name']
        address = connection['address']
        logger.info('Trying to connect to %s (SNMP).' %systemname)
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData('public', mpModel=0),
            cmdgen.UdpTransportTarget((address, 161)),
            cmdgen.MibVariable('SNMPv2-MIB', 'sysName', 0),
            lookupNames=True, lookupValues=True
        )
        if errorIndication:
            logger.warning(errorIndication)
        elif errorStatus:
            logger.warning(errorStatus)
        else:
            for name, val in varBinds:
                logger.info('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
        if errorIndication or errorStatus:
            logger.warning('%s test failure.' %systemname)
        else:
            logger.info('%s test successful.' %systemname)
    logger.info('FINISH')
    return


def main():
    run()


if __name__ == '__main__':
    main()
