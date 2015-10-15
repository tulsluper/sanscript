#!/usr/bin/env python3


import os
from settings import APPNAME, JSONDIR
from defs import dump_data
from san_db import save


def main():
    dump_data(
        os.path.join(JSONDIR, 'last_update'),
        [{'appname': APPNAME}]
    )
    save('sa', [
        ['last_update', 'AppDataLastUpdate', {'before_delete': {'appname': APPNAME}}],
    ])


if __name__ == '__main__':
    main()
