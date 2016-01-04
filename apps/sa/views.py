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
from .defs import create_formset, sfilter, stable
from django.views.decorators.csrf import csrf_protect
from apps.da.models import Capacity
from apps.fc.models import SwitchCommon, PortCommon
from apps.bc.models import SDicts, CDicts, PortConfig, Integers, Last
from django.db.models import Sum
from .forms import *
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings


def prevent_password_save(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass # object is new
    else:
        if not instance.password:
            instance.password = obj.password # do not change password
        elif instance.password.strip() == '':
            instance.password = None # set password to empty
    return



def dashboard(request):
    # da
    objs = Capacity.objects.all()
    if objs:
        FormattedUsed = int(list(objs.aggregate(Sum('FormattedUsed')).values())[0])
        FormattedAvailable = int(list(objs.aggregate(Sum('FormattedAvailable')).values())[0])
    else:
        FormattedUsed, FormattedAvailable = 0, 0
    # fc
    SwitchesCount = SwitchCommon.objects.count()
    PortsCount = PortCommon.objects.count()

    # bc
    try:
        data = Last.objects.last()
    except:
        data = {}
    tx_elements = data.get('tx_elements')
    integer = data.get('integer')
    active_ports_number = data.get('active_ports_number')

    data = {
        'FormattedUsed': FormattedUsed,
        'FormattedAvailable': FormattedAvailable,
        'SwitchesCount': SwitchesCount,
        'PortsCount': PortsCount,
        'tx_elements': tx_elements,
        'integer': integer,
        'active_ports_number': active_ports_number,
    }
    return render(request, 'dashboard.html', data)


def sa_admin(request):
    data = {}
    return render(request, 'home.html', data)


def home(request):
#    app_label = request.path.split('/')[1].split('-')[0]
    if request.path.split('/')[1] == 'sa':
        return dashboard(request)
    elif request.path.split('/')[1] == 'sa-sa':
        return sa_admin(request)
    else:
        return render(request, 'home.html', {})


def settings_view(request):
    custom_f = os.path.join(BASE_DIR, 'sanscript/custom_settings.py')
    if request.POST:
        lines = request.POST.get('text', '')
        with open(custom_f, 'w') as f:
            f.write(lines) 
    if os.path.isfile(custom_f) and os.path.getsize(custom_f) > 0:
        with open(custom_f) as f:
            lines = f.readlines() 
    else:
        with open(os.path.join(BASE_DIR, 'sanscript/custom_settings.tl')) as f:
            lines = f.readlines()
    data = {
        'lines': lines,
    }
    return render(request, 'settings.html', data)


@staff_member_required
def test_email_view(request):
    message = None
    if request.method == 'GET':
        form = EmailForm(initial={
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'subject': 'SANscript test email',
            'message': 'Hello!',
        })
    else:
        form = EmailForm(request.POST)
        if form.is_valid():
            to_email = form.cleaned_data['to_email']
            from_email = form.cleaned_data['from_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, [to_email])
                message = {'text': 'email sent successfully', 'type': 'success'}
            except Exception as e:
                message = {'text': 'Exception: {}'.format(e), 'type': 'warning'}
    return render(request, "test_email.html", {'form': form, 'message': message})


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
                    ['/usr/bin/python3', scriptfile],
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
        objects = sfilter(Model, request)
        cols, rows = stable(Model, objects)

        data.update({
            'cols': cols,
            'rows': rows,
        })
    return render(request, 'table.html', data)

