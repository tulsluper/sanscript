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
from settings import TEXTDIR


def get_content(enc_fqdn):
    url = 'http://'+enc_fqdn.rstrip()+'/xmldata?item=all'
    page = urllib.request.urlopen(url)
    content = page.read().decode('utf8')
    return content


def main():
    for connection in CONNECTIONS:
        try:
            content = get_content(connection['address'])
            filename = '%s.xmldata' %(connection['name'])
            filepath = os.path.join(TEXTDIR, filename)
            with open(filepath, 'w') as f:
                f.write(content)
                logging.info('%s | %s lines' %(filename, len(content)))
        except:
            logging.warning('%s data collection failed' %connection['name'])
    return


if __name__ == '__main__':
    main()
