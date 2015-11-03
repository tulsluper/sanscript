#!/usr/bin/env python3

import os
from datetime import datetime
from shutil import copyfile
from settings import JSONDIR, CONFIGSDIR
from defs import dump_data


def main():
    newpath = os.path.join(CONFIGSDIR, 'volumes_new')
    oldpath = os.path.join(CONFIGSDIR, 'volumes_old')

    if os.path.isfile(newpath):
        from_dt = datetime.fromtimestamp(os.path.getmtime(newpath))
        copyfile(newpath, oldpath)
    else:
        from_dt = None

    copyfile(os.path.join(JSONDIR, 'volumes'), newpath)
    till_dt = datetime.fromtimestamp(os.path.getmtime(newpath))

    dump_data(
        os.path.join(JSONDIR, 'volumes_changes_dts'),
        {'From': str(from_dt) if from_dt else None, 'Till': str(till_dt)}
    )
    

if __name__ == '__main__':
    main()

