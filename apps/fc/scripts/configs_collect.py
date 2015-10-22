#!/usr/bin/env python3

import os
from datetime import datetime
from settings import JSONDIR, CONFIGSDIR
from settings import fabrics_connections_path, newconfigpath, oldconfigpath
from defs import load_data, dump_data, ssh_run


import logging
logging.getLogger("paramiko").setLevel(logging.WARNING)



def parse_aliases(lines):
    out = {}
    block = False 
    for line in lines:
        if block and line == '':
            break
        if not block and line[1:6] == 'alias':
            block = True
        if block:
            items = line.replace(';', '').split()
            if line[1:6] == 'alias':
                alias = items[1]
                items = items[2:] if len(items) > 2 else []
                out[alias] = []
            out[alias] += items
    return out


def parse_zones(lines):
    out = {}
    block = False
    for line in lines:
        if block and line[1:6] == 'alias':
            break
        if not block and line[1:5] == 'zone':
            block = True
        if block:
            items = line.replace(';', '').split()
            if line[1:5] == 'zone':
                zone = items[1]
                items = items[2:] if len(items) > 2 else []
                out[zone] = []
            out[zone] += items
    return out


def parse_config(lines):
    out = {}
    effective = False
    block = False
    for line in lines:
        if line[:9] == 'Effective':
            effective = True
        if effective and line[1:5] == 'zone':
            block = True
        if block:
            items = line.replace(';', '').split()
            if line[1:5] == 'zone':
                zone = items[1]
                items = items[2:] if len(items) > 2 else []
                out[zone] = []
            out[zone] += items
    return out


def main():

    if not os.path.exists(CONFIGSDIR):
        os.makedirs(CONFIGSDIR)

    connections = load_data(fabrics_connections_path, [])
    fields = ['name', 'address', 'username', 'password']
    connections = [[c[k] for k in fields] for c in connections]

    out = {}
    for args in connections:
        args.append([['zoneshow', 'zoneshow'],])
        systemname, outs, errs, exception = ssh_run(args)
        if not exception:
            lines = outs['zoneshow'].split('\n')
            aliases = parse_aliases(lines)
            zones = parse_zones(lines)
            config = parse_config(lines)
            out[systemname] = {
                'aliases': aliases,
                'zones': zones,
                'config': config,
            }
    if os.path.isfile(oldconfigpath):
        from_dt = datetime.fromtimestamp(os.path.getmtime(oldconfigpath))
    else:
        from_dt = None
    if os.path.isfile(newconfigpath):
        os.rename(newconfigpath, oldconfigpath)
    till_dt = datetime.now()
    dump_data(newconfigpath, out)
    dump_data(os.path.join(JSONDIR, 'changes_dts'), {'From': str(from_dt) if from_dt else None, 'Till': str(till_dt)})
    logging.info('%s | %s records' %(newconfigpath, len(out)))
    return


if __name__ == '__main__':
    main()

