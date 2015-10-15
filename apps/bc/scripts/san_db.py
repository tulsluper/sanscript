#!/usr/bin/env python3

import os
import logging
from datetime import datetime
from settings import JSONDIR
from defs import load_data
from san_env import get_apps


def save_into_db(appname, relations):
    apps = get_apps()
    for filename, modelname, filters in relations:
        records = load_data(os.path.join(JSONDIR, filename), [])
        model = apps.get_model(app_label=appname, model_name=modelname)
        if filters.get('before_delete_all'):
            model.objects.all().delete()
        elif filters.get('before_delete'):
            model.objects.filter(**filters['before_delete']).delete()

        """
        if 'History' in modelname:
            for record in records:
                Date = record['Date'] if 'Date' in record else datetime.now().date()
                model.objects.filter(
                    Date__contains=Date,
                    Storage=record['Storage']
                ).delete()
        else:
            model.objects.all().delete()
        """
        model.objects.bulk_create([model(**record) for record in records])
        logging.info('--- file: %s -> model: %s | %s records' %(
            filename, modelname, len(records)))
    return
