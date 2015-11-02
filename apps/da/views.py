from django.shortcuts import render
from apps.sa.defs import sfilter, stable, sum_by_field
from django.db.models import Sum
from .models import *
from datetime import datetime, timedelta


def home(request):
    data = {}
    return render(request, 'home.html', data)


def capacity(request):
    objs = sfilter(Capacity, request)
    sum_row = sum_by_field(Capacity, objs)
    data = {
        'objs': objs,
        'sum_row': sum_row,
        'integer': 'TB',
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

