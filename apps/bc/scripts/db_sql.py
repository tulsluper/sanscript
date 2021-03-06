#!/usr/bin/env python3

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


def check_and_fix(uid, value):
    counter = uid.split()[-1]
    if counter in ['BBCreditZero', 'Error', 'InvalidOrderedSets'] and value > 2*10**9:
        value = -2 # error code 2
    return value


def round_to_1(value):
    if 0 < value < 1:
        return round(value, -int(floor(log10(value))))
    else:
        return int(value)


def to_scale(values, deltas, counter, itype):
    if counter in INTEGERS[itype]:
        integer = INTEGERS[itype][counter]
        scale = SCALES[integer.split('/')[0]]
        newvalues = []
        for value, delta in zip(values, deltas):
            if value <= 0:
                newvalues.append(value)
            else:
                delta = 1 if integer[-1] == 'd' else delta
                newvalues.append(round_to_1(value/delta/scale))
        return newvalues
    else:
        return values


def sum_udiffs(dirpath):
    udiffs, xtimes, deltas = {}, [], []
    filenames = os.listdir(dirpath)
    zeros = [0 for _ in filenames]
    for num, filename in enumerate(sorted(filenames)):
        _, xtime, delta = filename.split('.')
        xtimes.append(xtime.split('-'))
        deltas.append(int(delta))        
        filepath = os.path.join(dirpath, filename)
        data = load_data(filepath, {})
        for uid, value in data.items():
            if not uid in udiffs:
                udiffs[uid] = zeros[:]
            value = check_and_fix(uid, value)
            udiffs[uid][num] = value
    return udiffs, xtimes, deltas


def calc_dicts(udiffs, deltas):
    cdicts = defaultdict(dict)
    pdicts = defaultdict(dict)
    sdicts = {}
    for uid, values in udiffs.items():
        swport, counter = uid.rsplit(' ', 1)
        if not counter in sdicts:
            sdicts[counter] = [0 for _ in deltas]
        if sum(values):
            sdicts[counter] = [x+y if y>0 else x for x,y in zip(sdicts[counter], values)]
            values = to_scale(values, deltas, counter, 'p')
            cdicts[counter][swport] = values
            pdicts[swport][counter] = values
    for counter, values in sdicts.items():
        sdicts[counter] = to_scale(values, deltas, counter, 's')
    return cdicts, pdicts, sdicts

def sum_f_ports(cdicts):
    #f_list = []
    #ports = load_data(os.path.join(BASEDIR, 'data/fc/json/port'), [])
    #for port in ports:
    #    if port['Type'] == 'F-Port' and not 'NPIV' in port['Comment'] and not 'Trunk' in port['Comment']:
    #        f_list.append('{} {}'.format(port['Switch'], port['Index']))
    recs = load_data(os.path.join(BASEDIR, 'data/fc/json/port'), [])
    f_ports = ['{} {}'.format(r['Switch'], r['Index']) for r in recs if r['Type'] == 'F-Port']

    recs = load_data(os.path.join(BASEDIR, 'data/fc/json/link'), [])
    link_ports = ['{} {}'.format(r['Switch1'], r['Port1']) for r in recs]


    fdicts = {}
    for counter, swportvalues in cdicts.items():
        if not counter in fdicts:
            fdicts[counter] = []
        for swport, values in swportvalues.items():
            if swport in f_ports and not swport in link_ports:
                fdicts[counter].append(values)

    for counter, values in fdicts.items():
        fdicts[counter] = [sum(x) for x in zip(*values)]

    return fdicts


def main():

    if len(sys.argv) > 1:
        datestring = sys.argv[1]
    else:
        datestring = datetime.now().strftime('%Y-%m-%d')

    dirpath = os.path.join(DIFFSDIR, datestring)

    udiffs, xtimes, deltas = sum_udiffs(dirpath)
    cdicts, pdicts, sdicts = calc_dicts(udiffs, deltas)

    fdicts = sum_f_ports(cdicts)

    date = datetime.now().date()
    apps = get_apps()
    appname = 'bc'
    for values, modelname in [ 
        [xtimes, 'XTimes'],
        [deltas, 'Deltas'],
        [cdicts, 'CDicts'],
        [pdicts, 'PDicts'],
        [sdicts, 'SDicts'],
        [fdicts, 'FDicts'],
        [INTEGERS, 'Integers'],
    ]:
        model = apps.get_model(app_label=APPNAME, model_name=modelname)
        obj, created = model.objects.update_or_create(
            date=date, defaults={'values': values})
        logging.info('--- model: %s | %s records' %(
            modelname, len(values)))
    return



if __name__ == '__main__':
    main()
