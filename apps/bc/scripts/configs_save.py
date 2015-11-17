#!/usr/bin/env python3

from settings import APPNAME
from san_db import save


def main():
    relations = [
        ['configs', 'PortConfig',  {'before_delete_all': True}],
    ]
    save(APPNAME, relations)
    return


if __name__ == '__main__':
    main()

