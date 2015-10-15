#!/usr/bin/env python3

from settings import APPNAME
from san_db import save_into_db


def main():
    relations = [
        ['changes', 'ChangeHistory', {}],
    ]
    save_into_db(APPNAME, relations)
    return


if __name__ == '__main__':
    main()
