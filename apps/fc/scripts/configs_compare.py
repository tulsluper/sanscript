#!/usr/bin/env python3

import os
import logging
import json
from settings import newconfigpath, oldconfigpath, JSONDIR
from defs import load_data, dump_data


def compare_configs(config1, config2):
    records = []
    fabrics = config2.keys()
    parts = list(config2.values())[0].keys()
    for fabric in fabrics:
        data = {}
        if config1[fabric] != config2[fabric]:
            for part in parts:
                data[part] = {}
                records1 = config1[fabric][part]
                records2 = config2[fabric][part]
                if records1 != records2:
                    added = list(set(records2.keys()) - set(records1.keys()))
                    if added:
                        items = {key: records2[key] for key in added}
                        if items:
                            data[part]['added'] = items
                    removed = list(set(records1.keys()) - set(records2.keys()))
                    if removed:
                        items = {key: records1[key] for key in removed}
                        if items:
                            data[part]['removed'] = items
                    common = list(set(records1.keys()) & set(records2.keys()))
                    changed = [key for key in common if records1[key] != records2[key]]
                    if changed:
                        items = {key: [records1[key], records2[key]] for key in changed}
                        if items:
                            data[part]['changed'] = items
                if data[part] == {}:
                    del data[part]   
        if data:
            text = ''
            for section in ['aliases', 'zones', 'config']:
                if section in data:
                    text += '%s%s\n' %(' '*0, section)
                    for action in ['added', 'removed', 'changed']:
                        if action in data[section]:
                            text += '%s%s\n' %(' '*4, action)
                            for key, value in data[section][action].items():
                                if action == 'changed':
                                    value = '%s -> %s' %(value[0], value[1])
                                text += '%s%s: %s\n' %(' '*8, key, value)
    
            records.append({
                'Fabric': fabric,
                'Data': json.dumps(data),
                'Text': text,
            })
    return records


def main():
    config1 = load_data(oldconfigpath, {})
    config2 = load_data(newconfigpath, {})
    dts = load_data(os.path.join(JSONDIR, 'changes_dts'), {})
    if not config1:
        logging.warning('no config in %s' %oldconfigpath)
        logging.info('run collect_configs script again')
    if not config2:
        logging.warning('no config in %s' %newconfigpath)
    if config1 and config2:
        records = compare_configs(config1, config2)
        for record in records:
            record.update(dts)
        filepath = os.path.join(JSONDIR, 'changes')
        dump_data(filepath, records)
        logging.info('%s | %s records' %(filepath, len(records)))
    return


if __name__ == '__main__':
    main()
