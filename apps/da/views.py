from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from apps.sa.defs import sfilter, stable, sum_by_field, sum_by_field_to_list
from django.db.models import Sum
from .models import *
from .forms import *
from datetime import datetime, timedelta


def home(request):
    return redirect('/da/capacity/')


def capacity(request):
    objs = sfilter(Capacity, request)
    sum_row = sum_by_field(Capacity, objs)
    data = {
        'objs': objs,
        'sum_row': sum_row,
        'integer': 'TB',
        'visible_series': ['FormattedPresented', 'FormattedNotPresented', 'FormattedAvailable'],
    }
    return render(request, 'da/capacity.html', data)


def capacity_history(request):
    objs = sfilter(CapacityHistory, request)
    fields = CapacityHistory._meta.get_all_field_names()
    fields.remove('id')
    fields.remove('Storage')
    fields.remove('Date')
    fieldsvalues = {x: [] for x in fields}
    dates = sorted([x[0] for x in objs.values_list('Date').distinct()])
    storages = sorted([x[0] for x in objs.values_list('Storage').distinct()])
    for date in dates:
        date_objs = objs.filter(Date__contains=date)
        for field in fields:
            value = list(date_objs.aggregate(Sum(field)).values())[0]
            fieldsvalues[field].append(value)
    data = {
        'storages': storages,
        'dates': dates,
        'fieldsvalues': fieldsvalues,
        'visible_series': ['FormattedPresented'],
    }
    return render(request, 'da/capacity_history.html', data)


def capacity_3par_history(request):
    objs = sfilter(TPARCapacityHistory, request)
    fields = TPARCapacityHistory._meta.get_all_field_names()
    fields.remove('id')
    fields.remove('Storage')
    fields.remove('Date')
    fieldsvalues = {x: [] for x in fields}
    dates = sorted([x[0] for x in objs.values_list('Date').distinct()])
    storages = sorted([x[0] for x in objs.values_list('Storage').distinct()])
    for date in dates:
        date_objs = objs.filter(Date__contains=date)
        for field in fields:
            value = list(date_objs.aggregate(Sum(field)).values())[0]
            fieldsvalues[field].append(value)
    data = {
        'storages': storages,
        'dates': dates,
        'fieldsvalues': fieldsvalues,
        'visible_series': ['tpvv_used', 'tpvv_free'],
    }
    return render(request, 'da/capacity_3par_history.html', data)



def capacity_3par(request):
    objs = sfilter(TPARCapacity, request)
    data = {
        'objs': objs
    }
    return render(request, 'da/capacity_3par.html', data)


def volumes(request):
    objects = sfilter(Volume, request)
    cols, rows = stable(Volume, objects)
    for row in rows:
        #for value in row:
            value = row[2]
            if value.startswith('.'):
                row[2] = value.replace('.', '_')
    data = {
        'cols': cols,
        'rows': rows,
    }
    return render(request, 'table.html', data)


def hosts(request):
    objects = sfilter(Host, request)
    cols, rows = stable(Host, objects)
    data = {
        'cols': cols,
        'rows': rows,
    }
    return render(request, 'table.html', data)

def hosts_capacity(request):
    objects = sfilter(HostCapacity, request)
    cols, rows = stable(HostCapacity, objects)
    sum_row = sum_by_field_to_list(HostCapacity, objects, ['Size'])
    data = {
        'cols': cols,
        'rows': rows,
        'sum_row':sum_row,
    }
    return render(request, 'table.html', data)


def hosts_capacity_history(request):
    objs = sfilter(HostCapacityHistory, request)
    objs = objs.exclude(Hosts__startswith='[]')
    fields = HostCapacityHistory._meta.get_all_field_names()
    fields.remove('id')
    fields.remove('Storage')
    fields.remove('Date')

    cols, rows_ = stable(HostCapacityHistory, objs, fields=['Storage', 'Hosts'])

    rows = []
    for row in rows_:
        if not row in rows:
            rows.append(row)

    fieldsvalues = {x: [] for x in fields}
    dates = sorted([x[0] for x in objs.values_list('Date').distinct()])
    storages = sorted([x[0] for x in objs.values_list('Storage').distinct()])
    for date in dates:
        date_objs = objs.filter(Date__contains=date)
        for field in ['Size',]:
            value = list(date_objs.aggregate(Sum(field)).values())[0]
            value = value/1024
            fieldsvalues[field].append(value)
    data = {
        'storages': storages,
        'dates': dates,
        'fieldsvalues': fieldsvalues,
        'visible_series': ['Size'],
        'cols': cols,
        'rows': rows,
    }
    return render(request, 'da/hosts_capacity_history.html', data)


def changes(request):
    def ch_format(old, new):
        return '<del>{}</del> <span style class="t_red">>></span> <strong>{}</strong>'.format(old, new)

    objs = sfilter(VolumeChange, request)

    objs_x = objs.exclude(Action_Flag='new')
    for obj in objs_x:
        if obj.Action_Flag == 'old':
            try:
                new_obj = objs.get(Till=obj.Till, Storage=obj.Storage, Uid=obj.Uid, Action_Flag='new')
                if obj.Name != new_obj.Name:
                    obj.Name = ch_format(obj.Name, new_obj.Name)
                if obj.Size != new_obj.Size:
                    obj.Size = ch_format(obj.Size, new_obj.Size)
                if obj.Hosts != new_obj.Hosts:
                    obj.Hosts = ch_format(obj.Hosts, new_obj.Hosts)
            except:
                pass

    data = {
        'objs': objs_x,
    }
    return render(request, 'da/changes.html', data)


@csrf_protect
def change_acknowledge(request):
    id = request.GET.get('id')
    instance = VolumeChange.objects.get(id=id)
    form = VolumeChangeForm(request.POST or None, instance=instance)
    if form.is_valid():
          instance = form.save(commit=False)
          instance.Acknowledged = True
          instance.save()
          return redirect('/da/changes/')
    data = {
        'instance': instance,
        'form': form,
    }
    return render(request, 'da/change_acknowledge.html', data)


@csrf_protect
def change_delete(request):
    id = request.GET.get('id')
    obj = VolumeChange.objects.get(id=id)
    objs = VolumeChange.objects.filter(Storage=obj.Storage, Uid=obj.Uid, From=obj.From, Till=obj.Till)
    objs.delete()
    return redirect('/da/changes/')

