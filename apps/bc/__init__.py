import os


dirpath = os.path.dirname(os.path.realpath(__file__))
if os.path.isfile(os.path.join(dirpath, 'apps.py')):
    app_label = os.path.basename(dirpath)
    default_app_config = 'apps.{}.apps.appAppConfig'.format(app_label)
