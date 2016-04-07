from django.shortcuts import render
from apps.sa.defs import sfilter, stable
from .models import *


def home(request):
    return render(request, 'home.html')


def enclosures(request):
    objs = sfilter(Enclosure, request)
    cols, rows = stable(Enclosure, objs)
    data = {
        'cols': cols,
        'rows': rows,
    }
    return render(request, 'table.html', data)


def servers(request):
    objs = sfilter(Server, request)
    cols, rows = stable(Server, objs)
    cols0 = [col.replace('_', ' ') for col in cols]
    data = {
        'cols': cols0,
        'cols': cols,
        'rows': rows,
    }
    return render(request, 'en/table.html', data)


def mezzanines(request):
    objs = sfilter(Mezzanine, request)
    cols, rows = stable(Mezzanine, objs)
    data = {
        'cols': cols,
        'rows': rows,
    }
    return render(request, 'table.html', data)

