#!/usr/bin/env python3

import os
import logging
import subprocess
import tempfile
import shutil
from defs import load_data, ssh_run
from settings import logging
from settings import EVA_CLI, TEXTDIR
from settings import COMMANDS_EVA as COMMANDS

dirpath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(dirpath, 'StorageConnection.json')
CONNECTIONS = load_data(filepath, [])


def main():
    for connection in CONNECTIONS:
        if connection['model'] == 'EVA':
            systemname = connection['name']
            args = [connection[key] for key in ['address', 'username', 'password']]
            connect_line = 'SELECT MANAGER %s USERNAME=%s PASSWORD=%s' %tuple(args)

            for commandname, command in COMMANDS:
                filename = '%s.%s' %(systemname, commandname)
                filepath = os.path.join(TEXTDIR, filename)
                with open(filepath, 'w') as f:
    
                    script = tempfile.NamedTemporaryFile()
                    cli_commands = [
                        connect_line,
                        'select system %s' %systemname, command, 'exit']
                    script.write(bytes('\n'.join(cli_commands), 'utf-8'))
                    script.seek(0)
    
                    p = subprocess.Popen([EVA_CLI, 'file %s' %script.name],
                        stdout=subprocess.PIPE)
                    out = p.stdout.read().decode("utf-8")
                    f.write(out)
                    p.communicate()
    
                    logging.info('%s | %s lines' %(
                        filename, len(out.strip().split('\n'))))

    for dirname in ['logs', 'cache']:
        dirpath = os.path.join(os.getcwd(), dirname)
        if os.path.isdir(dirpath):
            shutil.rmtree(dirpath)

    return


if __name__ == '__main__':
    main()
