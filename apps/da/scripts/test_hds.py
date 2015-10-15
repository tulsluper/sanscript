#!/usr/bin/env python3

import os
import subprocess
from defs import load_data
from settings import logging
from settings import HDS_CLI

dirpath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(dirpath, 'StorageConnection.json')
CONNECTIONS = load_data(filepath, [])


def main():

    os.environ['LD_LIBRARY_PATH'] = os.path.join(HDS_CLI, 'lib')
    os.environ['STONAVM_HOME'] = HDS_CLI

    for connection in CONNECTIONS:
        if connection['model'] == 'HDS':
            systemname = connection['name']
            address = connection['address']
            username = connection['username']
            password = connection['password']

            clicommand = '%s/auunitadd -unit %s -ctl0 %s' %(HDS_CLI, systemname, address)
            p = subprocess.Popen(clicommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = p.stdout.read().decode("utf-8")
            p.communicate()

            authcommand = "printf %s\\n%s" %(username, password)
            clicommand = "%s/%s -unit %s" %(HDS_CLI, 'auunitinfo', systemname)
            auth = subprocess.Popen(authcommand.split(), stdout=subprocess.PIPE)
            p = subprocess.Popen(
                clicommand.split(),
                stdin=auth.stdout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            out = p.stdout.read().decode("utf-8")
            err = p.stderr.read().decode("utf-8").strip()
            p.communicate()
    
            if not out and err:
                logging.warning('%s test failed - %s' %(systemname, err.split('\n')[-1]))
            else:
                logging.info('%s test success' %systemname)

    return


if __name__ == '__main__':
    main()
