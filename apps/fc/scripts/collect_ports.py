#!/usr/bin/env python3

import os
import logging
from datetime import datetime
from multiprocessing import Pool
from contextlib import closing
from defs import load_data, ssh_run
from settings import PROCESSES, P_COMMANDS, TEXTDIR, ARCHDIR

logging.getLogger("paramiko").setLevel(logging.WARNING)

fields = ['name', 'address', 'username', 'password']
dirpath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(dirpath, 'SwitchConnection.json')
connections = load_data(filepath, [])
S_CONNECTIONS = [[c[k] for k in fields] for c in connections]


def switchshow_to_ports(lines):
    ports = []
    notslot = False
    portline = False
    for line in lines:
        if portline:
            values = line.split()
            if notslot:
                values.insert(1,'')
            uPort = '/'.join(values[1:3]) if values[1] else values[2]
            ports.append(uPort)
        elif line[:5] == 'Index' and not 'Slot' in line:
            notslot = True
        elif line[:4] == 'Area':
            notslot = True
        elif line[0] == '=':
            portline = True
    return ports


def main():

    swports = {}
    for filename in os.listdir(TEXTDIR):
        filepath = os.path.join(TEXTDIR, filename)
        system, command = filename.split('.')
        if command == 'switchshow':
            with open(filepath) as f:
                lines = f.readlines()
                swports[system] = switchshow_to_ports(lines)

    args = []
    for connection in S_CONNECTIONS:
        system = connection[0]
        ports = swports.get(system)
        if ports:
            for commandname, command in P_COMMANDS:
                portscommand = [['%s %s' %(command, port), '%s %s' %(command, port)] for port in ports]
                args.append(connection + [portscommand])

    with closing(Pool(PROCESSES)) as pool:
        for result in pool.imap_unordered(ssh_run, args):
            system, outs, errs, exception = result
            command_outs = {}
            if not exception:
                for command_port, out in outs.items():
                    command, port = command_port.split()
                    if not command in command_outs:
                        command_outs[command] = ''
                    command_outs[command] += '\n*%s\n%s' %(port, out)
            else:
                logging.warning('%s %s' %(system, exception))
            for command, out in command_outs.items():
                filename = '%s.%s' %(system, command)
                filepath = os.path.join(TEXTDIR, filename)
                with open(filepath, 'w') as f:
                    f.write(out)
                    logging.info('%s | %s lines' %(filename, len(out)))

    return


if __name__ == '__main__':
    main()


