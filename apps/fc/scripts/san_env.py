#!/usr/bin/env python3

import os
import sys
import django
from settings import BASEDIR


def get_apps():
    sys.path.append(BASEDIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sanscript.settings")
    django.setup()
    from django.apps import apps
    return apps
