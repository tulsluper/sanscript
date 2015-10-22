#!/usr/bin/env python3

from settings import APPNAME
from san_db import save


def main():
    relations = [
        ['changes', 'Change', {}],
    ]
    save(APPNAME, relations)
    return


if __name__ == '__main__':
    main()
