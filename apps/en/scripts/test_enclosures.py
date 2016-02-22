#!/usr/bin/env python3

import os
from defs import load_data, ssh_run
from settings import logging
import urllib.request
import xmltodict

logging.getLogger("paramiko").setLevel(logging.WARNING)

dirpath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(dirpath, 'Connection.json')
CONNECTIONS = load_data(filepath, [])


def get_data(enc_fqdn):
    url = 'http://'+enc_fqdn.rstrip()+'/xmldata?item=all'
    page = urllib.request.urlopen(url)
    content = page.read().decode('utf8')
    data = xmltodict.parse(content)
    return data


def main():
    for connection in CONNECTIONS:
        try:
            data = get_data(connection['address'])
            Name = data['RIMP']['INFRA2']['ENCL'],
            SN = data['RIMP']['INFRA2']['ENCL_SN'],
            Location = data['RIMP']['INFRA2']['RACK']
            logging.info('{} test success ({} {} {})'.format(connection['name'], Name, SN, Location))
        except:
            logging.warning('%s test failed' %connection['name'])
    return


if __name__ == '__main__':
    main()
