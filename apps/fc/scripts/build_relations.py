#!/usr/bin/env python3

import os
from settings import logging
from settings import JSONDIR
from defs import load_data, dump_data
from collections import defaultdict


def get_swport(wwn):
    try:
        p = Port.objects.get(Wwn=wwn)
        swport = '%s %s' %(p.Switch, p.Index)
    except Port.DoesNotExist:
        try:
            p = Portshow.objects.get(portWwn_of_devices_connected__contains=wwn)
            swport = '%s %s' %(p.Switch, p.portIndex)
        except Port2.DoesNotExist:
            swport = None
    return swport


def form_rels(zones, aliases, ports, portshow):

    alirelations = defaultdict(set)
    swport_alias = defaultdict(set)
    alias_swport = defaultdict(set)

    aliasesD = {'%s %s' %(r['Fabric'], r['Name']): r['Wwns'] for r in aliases }
    portsD = {r['Wwn']: '%s %s' %(r['Switch'], r['Index']) for r in ports}
    for r in portshow:
        for wwn in r['portWwn_of_devices_connected']:
            if not wwn in portsD:
                portsD[wwn] = '%s %s' %(r['Switch'], r['portIndex'])
    #portsD.update({r['portWwn_of_devices_connected']: '%s %s' %(r['Switch'], r['portIndex']) for r in portshow})

    for zone in zones:
        fabric = zone['Fabric']
        aliases = zone['Aliases']
    
        for alias in aliases:
    
            fab_alias = '%s %s' %(fabric, alias)
            rels = ['%s %s' %(fabric, a) for a in aliases if a != alias]
            alirelations[fab_alias] |= set(rels)
    
            wwns =  aliasesD.get('%s %s' %(fabric, alias), [])
            for wwn in wwns:
                swport = portsD.get(wwn)
                if swport:
                    swport_alias[swport].add(fab_alias)
                    alias_swport[fab_alias].add(swport)

    return alirelations, swport_alias, alias_swport


def form_swport_rels(alirelations, alias_swport):

    swportrelations = defaultdict(set)

    for alias, aliases in alirelations.items():
        swports1 = alias_swport[alias]
        swports2 = set()
        for alias in aliases:
            swports2 |= alias_swport[alias]
    
        for swport in swports1:
            swportrelations[swport] |= swports2
    for k, v in swportrelations.items():
        swportrelations[k] = [x for x in v if x != k]
    
    return swportrelations


def main():

    filepath = os.path.join(JSONDIR, 'zone')
    zones = load_data(filepath, [])
    filepath = os.path.join(JSONDIR, 'alias')
    aliases = load_data(filepath, [])
    filepath = os.path.join(JSONDIR, 'port')
    ports = load_data(filepath, [])
    filepath = os.path.join(JSONDIR, 'portshow')
    portshow = load_data(filepath, [])

    alirelations, swport_alias, alias_swport = form_rels(zones, aliases, ports, portshow)
    swportrelations = form_swport_rels(alirelations, alias_swport)


    records = []
    for swport, aliases in swport_alias.items():
        aliases = [a.split()[1] for a in aliases]
        records.append({'Swport': swport, 'Aliases': aliases})
    filepath = os.path.join(JSONDIR, 'swport_alias')
    dump_data(filepath, records)
    logging.info('%s | %s records' %('swport_alias', len(records)))

    records = []
    for alias, swports in alias_swport.items():
        records.append({'Alias': alias, 'Swports': list(swports)})
    filepath = os.path.join(JSONDIR, 'alias_swport')
    dump_data(filepath, records)
    logging.info('%s | %s records' %('alias_swport', len(records)))

    records = []
    for port, relation in swportrelations.items():
        records.append({'Port': port, 'Relation': relation})
    filepath = os.path.join(JSONDIR, 'port_relation')
    dump_data(filepath, records)
    logging.info('%s | %s records' %('port_relation', len(records)))


    filepath = os.path.join(JSONDIR, 'rels')
    dump_data(filepath, swportrelations)


if __name__ == '__main__':
    main()




