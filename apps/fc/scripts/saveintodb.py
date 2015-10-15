#!/usr/bin/env python3

from settings import APPNAME, MODELS
from san_db import save_into_db


def main():
    save_into_db(APPNAME, MODELS)


if __name__ == '__main__':
    main()
