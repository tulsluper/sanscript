#!/usr/bin/env python3

"""
import os
import sys
import json
import logging
from collections import defaultdict
from datetime import datetime
from settings import SCALES, INTEGERS, APPNAME, DIFFSDIR, BASEDIR
from defs import load_data, dump_data
from math import log10, floor
from san_env import get_apps
"""
import os
import json
from defs import dump_data
from settings import APPNAME, JSONDIR
from san_env import get_apps


def main():

    try:
        SDicts = get_apps().get_model(app_label=APPNAME, model_name='SDicts')
        CDicts = get_apps().get_model(app_label=APPNAME, model_name='CDicts')
        Integers = get_apps().get_model(app_label=APPNAME, model_name='Integers')
        Last = get_apps().get_model(app_label=APPNAME, model_name='Last')

        tx_elements = SDicts.objects.last().values.get('TxElements', [])[-1]
        integer = Integers.objects.last().values['s']['TxElements']

        ports_values = CDicts.objects.last().values.get('TxElements')
        active_ports_number = len([1 for xlist in ports_values.values() if xlist[-1]])
    except:
        tx_elements = None
        integer = None
        active_ports_number = None

    data = {
        'tx_elements': tx_elements,
        'integer': integer,
        'active_ports_number': active_ports_number,
    }

    Last.objects.all().delete()
    obj = Last(values=data)
    obj.save()

#    dump_data(os.path.join(JSONDIR, 'last_values'), data)


if __name__ == '__main__':
    main()
