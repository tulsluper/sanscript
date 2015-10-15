from django.shortcuts import render
from apps.sa.defs import build_filters, model_to_table
from django.db.models import Sum
from .models import *
from datetime import datetime, timedelta


def home(request):
    data = {}
    return render(request, 'home.html', data)

def capacity(request):
    filters = build_filters(request)
    objs = Capacity.objects.filter(**filters)
    data = {
        'objs': objs
    }
    return render(request, 'da/capacity.html', data)


def capacity_history(request):
    filters = build_filters(request)
    objs = CapacityHistory.objects.filter(**filters)
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
    filters = build_filters(request)
    objs = TPARCapacityHistory.objects.filter(**filters)
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
    TPARCapacity.objects.all()
    data = {
        'objs': TPARCapacity.objects.all()
    }
    return render(request, 'da/capacity_3par.html', data)


def volumes(request):
    filters = build_filters(request)
    cols, rows = model_to_table(Volume, filters)
    data = {
        'cols': cols,
        'rows': rows,
    }
    return render(request, 'table.html', data)


def hosts(request):
    filters = build_filters(request)
    cols, rows = model_to_table(Host, filters)
    data = {
        'cols': cols,
        'rows': rows,
    }
    return render(request, 'table.html', data)

