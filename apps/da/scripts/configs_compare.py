#!/usr/bin/env python3

import os
import logging
import json
from settings import JSONDIR, CONFIGSDIR
from defs import load_data, dump_data


def compare_configs(config1, config2):
    data = {}

    
    if config1 != config2:
        records1 = {'{} {}'.format(r['Storage'], r['Uid']): r for r in config1}
        records2 = {'{} {}'.format(r['Storage'], r['Uid']): r for r in config2}

        added = list(set(records2.keys()) - set(records1.keys()))
        if added:
            data['added'] = [records2[key] for key in added]

        removed = list(set(records1.keys()) - set(records2.keys()))
        if removed:
            data['removed'] = [records1[key] for key in removed]

        common = list(set(records1.keys()) & set(records2.keys()))
        changed = [[records1[key], records2[key]] for key in common if records1[key] != records2[key]]
        if changed:
            data['changed'] = []
            for pair in changed:
                pair[0]['Action_Flag'] = 'old'
                pair[1]['Action_Flag'] = 'new'
                data['changed'] += pair

    records = []
    for key in ['added', 'removed', 'changed']:
        if key in data:
            for record in data[key]:
                if not record['Name'].startswith("rcpy."):
            #    if '_' in key:
            #        action, action_flag = key.split('_', 1)
            #    else:
            #        action, action_flag = key, ''
            #    print(action, action_flag)
                    record['Action'] = key
            #    record.update({'Action': action, 'Action_Flag': action_flag})
                    records.append(record)

    return records


def main():
    oldpath = os.path.join(CONFIGSDIR, 'volumes_old')
    newpath = os.path.join(CONFIGSDIR, 'volumes_new')
    config1 = load_data(os.path.join(CONFIGSDIR, 'volumes_old'), {})
    config2 = load_data(os.path.join(CONFIGSDIR, 'volumes_new'), {})
    dts = load_data(os.path.join(JSONDIR, 'volumes_changes_dts'), {})
    if not config1:
        logging.warning('no config in %s' %oldpath)
        logging.info('run collect_configs script again')
    if not config2:
        logging.warning('no config in %s' %newpath)
    if config1 and config2:
        records = compare_configs(config1, config2)
        for record in records:
            record.update(dts)
            print(record)
        filepath = os.path.join(JSONDIR, 'volumes_changes')
        dump_data(filepath, records)
        logging.info('%s | %s records' %(filepath, len(records)))
    return


if __name__ == '__main__':
    main()
