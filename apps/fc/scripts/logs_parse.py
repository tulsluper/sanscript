#!/usr/bin/env python3

import os
import json
from datetime import datetime, timedelta
from settings import TEMPDIR, TEXTDIR, JSONDIR
from settings import logging
from defs import dump_data, load_data

def fix_items(items, line):

    if len(items) == 5:
        items.append('')

    elif len(items) > 6:
        items[5] = ' '.join(items[5:])
        del items[6:]
        if ',' in items[4]:
            items[5] = ' '.join(items[4:])
            items[4] = ''

    port = items[3]
    if len(port) > 10:
        items[3] = port[:-8]
        items[4] = port[-8:]
    elif len(port) > 4:
        new = line[:35].split()[-1]
        items[3] = new
        items[4] = port[len(new):]

    return items


def to_items(switch, lines, last_dt):
    records = []
#    actual = False
    dt = None
    for line in lines:
        if line[3] == ' ':
            items = line.strip().split()
            xdate = ' '.join([items[x] for x in [1, 2, 4]])
            xdate_date = datetime.strptime(xdate, '%b %d %Y').date()
#            if datetime.strptime(xdate, '%b %d %Y').date() >= last_dt.date():
#                actual = True
        else:
            if xdate_date > last_dt.date() or (xdate_date == last_dt.date() and line[:12] >= str(last_dt.time())[:12]):
#            if actual and line[:12] >= str(last_dt.time())[:12]:
                items = line.strip().split()
                items = fix_items(items, line)
                xtime, task, event, port, cmd, args = items
                dt = datetime.strptime(xdate+xtime, '%b %d %Y%H:%M:%S.%f')
                records.append({'dt': str(dt), 'switch': switch, 'port': port, 'task': task, 'event': event, 'cmd': cmd, 'args': args})
    return records, dt or last_dt


def to_items_fab(switch, lines, last_dt):
    records = []
    dt = None
    for line in lines:
        items = line.strip().split()
        if items[0] == 'Switch':
            xdate = ' '.join([items[x] for x in [3, 4, 6]])
        elif items[0] in ['Number', 'Max']:
            pass
        else:
            xtime = items[0]
            action = ' '.join(items[1:-4])
            S_P, Sn_Pn, Port, Xid = items[-4:]
            dt = datetime.strptime('%s %s' %(xdate, xtime), '%b %d %Y %H:%M:%S.%f')
            if last_dt is None or dt > last_dt:
                records.append({'dt': str(dt), 'switch': switch, 'action': action, 'S_P': S_P, 'Sn_Pn': Sn_Pn, 'Port': Port, 'Xid': Xid})
    return records, dt or last_dt


def main():

    null_dt = datetime.now()-timedelta(hours=1)
    last_dates = load_data(os.path.join(TEMPDIR, 'last_dates'), {})
    portlog = []
    fabriclog = []
    for filename in os.listdir(TEXTDIR):
        filepath = os.path.join(TEXTDIR, filename)
        system, command = filename.split('.')
        if command in ['portlogdump', 'fabriclog']:
            xdate = None
            with open(filepath) as f:
                records = []
                lines = f.readlines()

                last_dt_str = last_dates.get(filename)
                if last_dt_str is None:
                    last_dt = null_dt
                else:
                    last_dt = datetime.strptime(last_dt_str, "%Y-%m-%d %H:%M:%S")

                xdate = None
                if command == 'portlogdump':
                    records, xdate = to_items(system, lines[2:], last_dt)
                    portlog += records
                elif command == 'fabriclog':
                    records, xdate = to_items_fab(system, lines[2:-2], last_dt)
                    fabriclog += records
            dt_str = None if xdate is None else xdate.strftime("%Y-%m-%d %H:%M:%S")
            last_dates['{}.{}'.format(system, command)] = dt_str
    print(len(portlog))
    dump_data(os.path.join(TEMPDIR, 'last_dates'), last_dates)
    dump_data(os.path.join(JSONDIR, 'portlog'), portlog)
    dump_data(os.path.join(JSONDIR, 'fabriclog'), fabriclog)

    return

if __name__ == '__main__':
    main()
