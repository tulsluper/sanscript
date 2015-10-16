import os
import json
from sanscript.settings import BASE_DIR

import sys
import subprocess
from time import sleep

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.apps import apps
from django.db.models.signals import pre_save
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_protect
from django.contrib.admin.views.decorators import staff_member_required
from .defs import prevent_password_save, create_formset
from .defs import build_filters, model_to_table


def home(request):
    return render(request, 'home.html')


@staff_member_required
@csrf_protect
def v_configs(request, item_label=None):
    app_label = request.path.split('/')[1].split('-')[0]
    app = apps.get_app_config(app_label)
    try:
        items = app.config_models
    except AttributeError:
        items = []
    data = {
        'items': items,
    }
    if item_label:
        Model = app.get_model(item_label)
        if 'password' in Model._meta.get_all_field_names():
            pre_save.connect(prevent_password_save, sender=Model)
        FormSet = create_formset(Model)
        if request.method == 'POST':
            formset = FormSet(request.POST)
            if formset.is_valid():
                formset.save()

                connections = []
                fields = ['name', 'address', 'username', 'password', 'model', 'number']
                fields = list(set(fields) & set(Model._meta.get_all_field_names()))
                for instance in Model.objects.all():
                    connections.append(model_to_dict(instance, fields=fields))

                basepath = os.path.join(BASE_DIR, 'apps', app_label, 'scripts', item_label)
                filepath = basepath + '.json'
                with open(filepath, 'w') as f:
                    json.dump(connections, f, indent=4)

                return redirect(request.path)
        else:
            formset = FormSet()
        data.update({
            'formset': formset,
        })
    return render(request, 'sa/config.html', data)


@staff_member_required
@csrf_protect
def v_commands(request, item_label=None):

    app_label = request.path.split('/')[1].split('-')[0]
    app = apps.get_app_config(app_label)

    item = None
    try:
        items = app.commands
        for i in items:
            if item_label == i['label']:
                item = i
                break
    except AttributeError:
        items = []
    data = {
        'items': items,
        'item': item,
    }

    progress = False
    lines = []

    if item_label:
        basepath = os.path.join(BASE_DIR, 'apps', app_label, 'scripts', item_label)
        scriptfile = basepath + '.py'
        logfile = basepath + '.log'
        lockfile = basepath + '.lock'

        if not os.path.isfile(scriptfile):
            lines = ['ERROR Script %s not found' %scriptfile,]

        if os.path.isfile(logfile):
            with open(logfile) as f:
                lines = f.readlines()
        progress = os.path.isfile(lockfile)

        if request.GET.get('start'):
            if not progress:
                subprocess.Popen(
                    [sys.executable, scriptfile],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                sleep(1)
            return redirect(request.path)

        if request.is_ajax():
            position = int(request.POST.get('position', 0))
            lines = lines[position:]
            lines = [line.replace(' ', '&nbsp;').replace('\n', '<br>') for line in lines]
            data = {
                'progress': progress,
                'lines': lines,
            }
            return HttpResponse(json.dumps(data))
    data.update({
        'progress': progress,
        'lines': lines,
    })
    return render(request, 'sa/command.html', data)


@staff_member_required
@csrf_protect
def v_tables(request, item_label=None):
    app_label = request.path.split('/')[1].split('-')[0]
    app = apps.get_app_config(app_label)
    try:
        items = app.show_models
    except AttributeError:
        items = []
    data = {
        'items': items
    }
    if item_label:
        Model = app.get_model(item_label)
        filters = build_filters(request)
        cols, rows = model_to_table(Model, filters)
        data.update({
            'cols': cols,
            'rows': rows,
        })
    return render(request, 'table.html', data)

