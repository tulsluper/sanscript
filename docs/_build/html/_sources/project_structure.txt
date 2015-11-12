****************************
  Project Structure 
****************************

This is a simple example
:: 

    ├── apps			# project-specific applications
    ├── configs			# configs for deployment
    ├── data			# collected and parsed data
    ├── docs			# documentation
    ├── fixtures		# initial data for models
    ├── LICENSE			# license text
    ├── manage.py		# utility for administrative tasks
    ├── README.md		
    ├── requirements.txt	# list of required packages
    ├── sanscript		# actual Python package for project
    ├── services		
    ├── staticfiles		# static files
    └── templates		# html templates


apps/
===============

Project-specific applications::

    apps/
    ├── bc			# BCounters
    ├── da			# Disk Array (Storages)
    ├── fc			# Fibre Channel (Switches)
    └── sa			# admin module for apps

configs/
==================
configs for deployment::

    configs/
    ├── db_init_postgres.sql
    ├── nginx
    │   └── sanscript.conf
    └── uwsgi
        └── sanscript.ini

apps/<app_label>/
==================
::

    apps/<app_label>/
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── __init__.py
    ├── models.py
    ├── scripts/
    ├── tests.py
    ├── urls.py
    └── views.py

