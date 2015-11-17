#!/usr/bin/env python3

import os
import logging
from datetime import datetime
from settings import JSONDIR
from defs import load_data
from san_env import get_apps

debug_records_flag = False


def save(appname, relations):
    apps = get_apps()
    for filename, modelname, filters in relations:
        records = load_data(os.path.join(JSONDIR, filename), [])
        model = apps.get_model(app_label=appname, model_name=modelname)
        if filters.get('before_delete_all'):
            model.objects.all().delete()
        elif filters.get('before_delete'):
            model.objects.filter(**filters['before_delete']).delete()
        if debug_records_flag is False:
            model.objects.bulk_create([model(**record) for record in records])
        else:
            for record in records:
                try:
                    model(**record).save()
                except:
                    print('== {} =='.format(modelname))
                    for key in sorted(record.keys()):
                        print(key, record[key] if key in record else '')
                    print('\n')
        logging.info('--- file: %s -> model: %s | %s records' %(
            filename, modelname, len(records)))
    return
