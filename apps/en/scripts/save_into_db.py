#!/usr/bin/env python3

from settings import APPNAME, MODELS
from san_db import save


def main():
    save(APPNAME, MODELS)


if __name__ == '__main__':
    main()
