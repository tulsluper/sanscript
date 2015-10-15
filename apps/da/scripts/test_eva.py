#!/usr/bin/env python3

import os
import subprocess
import tempfile
import shutil
from defs import load_data, ssh_run
from settings import logging
from settings import EVA_CLI

dirpath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(dirpath, 'StorageConnection.json')
CONNECTIONS = load_data(filepath, [])


def main():
    for connection in CONNECTIONS:
        if connection['model'] == 'EVA':
            system = connection['name']
            args = [connection[key] for key in ['address', 'username', 'password']]
            connect_line = 'SELECT MANAGER %s USERNAME=%s PASSWORD=%s' %tuple(args)
    
            script = tempfile.NamedTemporaryFile()
            cli_commands = [
                connect_line,
               'select system %s' %system, 'exit']
            script.write(bytes('\n'.join(cli_commands), 'utf-8'))
            script.seek(0)
    
            p = subprocess.Popen([EVA_CLI, 'file %s' %script.name],
                stdout=subprocess.PIPE)
            out = p.stdout.read().decode("utf-8")
            p.communicate()
    
            err = ''.join([line for line in out.split('\n') if 'Error' in line])
            if err:
                logging.warning('%s test failed - %s' %(system, err))
            else:
                logging.info('%s test success' %system)

    for dirname in ['logs', 'cache']:
        dirpath = os.path.join(os.getcwd(), dirname)
        if os.path.isdir(dirpath):
            shutil.rmtree(dirpath)

    return


if __name__ == '__main__':
    main()
