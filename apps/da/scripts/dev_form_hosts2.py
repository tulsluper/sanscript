#!/usr/bin/env python3

import os
import logging
from settings import JSONDIR
from defs import load_data, dump_data


def main():
    unique_hosts = {}
    hosts = load_data(os.path.join(JSONDIR, 'hosts'), [])
    for host in hosts:
        wwns_uid = ' '.join(sorted(host['WWNs']))
        if not wwns_uid in unique_hosts:
            unique_hosts[wwns_uid] = []
        unique_hosts[wwns_uid].append(host)

    for key, hosts in unique_hosts.items():
        if len(hosts) > 1:
            print(hosts)
            print('')

"""
class Host(models.Model):
    Storage = models.CharField(max_length=30)
    Host = models.CharField(max_length=30)
    OS = models.CharField(max_length=30)
    WWNs = JSONField()
"""

    

if __name__ == '__main__':
    main()

