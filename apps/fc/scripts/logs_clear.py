#!/usr/bin/env python3

from datetime import datetime, timedelta
from san_env import get_apps


def main():
    null_dt = datetime.now()-timedelta(days=1, hours=1)
    Portlog = get_apps().get_model(app_label='fc', model_name='Portlog')
    Portlog.objects.filter(dt__lt=null_dt).delete()
    null_dt = datetime.now()-timedelta(days=366, hours=1)
    Fabriclog = get_apps().get_model(app_label='fc', model_name='Fabriclog')
    Fabriclog.objects.filter(dt__lt=null_dt).delete()
    return

if __name__ == '__main__':
    main()
