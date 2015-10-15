from datetime import datetime
from django.shortcuts import render, redirect
from pymongo import MongoClient
from .models import CounterOid
from apps.fc.models import Portshow
from .models import XTimes, Integers, SDicts, CDicts, PDicts

COUNTERS = [obj.name for obj in CounterOid.objects.all() if obj.enabled]

DBHOST = 'localhost'
DBNAME = 'bcounters'


def home(request):
    data = {}
    return render(request, 'home.html', data)


def sort_counters(counters, COUNTERS=COUNTERS):
    counters = list(counters)
    counters.sort(key=lambda x: COUNTERS.index(x))
    return counters


def dict_to_rows(xdict, integers={}):
    rows = []
    if xdict:
        for name in COUNTERS:
            integer = integers.get(name, '')
            values = xdict.get(name, None)
            if values and sum(values) > 0:
                rows.append([name, values, integer])
    return rows

# ==============================================================================


def port_view(request):
    datestring = request.GET.get('date')
    port = request.GET.get('port')
    if datestring is None:
        return redirect('%s?date=%s' %(request.path, datetime.now().strftime('%Y-%m-%d')))
    xtimes = XTimes.objects.get(date=datestring).values
    integers = Integers.objects.get(date=datestring).values
    if port:
        port = port.replace('_', ' ')
        pdicts = PDicts.objects.get(date=datestring).values
        pdicts = pdicts.get(port, {})
        rows = dict_to_rows(pdicts, integers['p'])
    else:
        sdicts = SDicts.objects.get(date=datestring).values
        rows = dict_to_rows(sdicts, integers['s'])
    ports = []
    for p in Portshow.objects.all():
        ports.append(['%s %s' %(p.Switch, p.portIndex), p.portName])
    data = {
        'datestring': datestring,
        'xtimes': xtimes,
        'rows': rows,
        'ptype': 'counter',
        'ports': ports,
        'port': port,
    }
    return render(request, 'bc/date.html', data)


def counter_view(request):
    datestring = request.GET.get('date')
    if datestring is None:
        return redirect('%s?date=%s' %(request.path, datetime.now().strftime('%Y-%m-%d')))
    xtimes = XTimes.objects.get(date=datestring).values
    integers = Integers.objects.get(date=datestring).values

    if request.is_ajax():
        datestring = request.POST['datestring']
        cdicts = CDicts.objects.get(date=datestring).values
        data = {
            'xtimes': xtimes,
            'counters': sort_counters(cdicts.keys()),
        }
        return HttpResponse(json.dumps(data))

    cdicts = CDicts.objects.get(date=datestring).values

    counter = request.GET.get('counter', '')
    sort = request.GET.get('sort', 'sum')
    port = request.GET.get('filter', '')
    quantity = request.GET.get('quantity', 10)

    if cdicts is None:
        cdicts = {}

    records = []
    for key, values in cdicts.get(counter, {}).items():
        sw, po = key.split()
        try:
            ports_objs = Portshow.objects.filter(Switch=sw, portIndex=po)
            if ports_objs:
                port_name = ports_objs[0].portName
            else:
                port_name = '?'
        except:
            port_name = '?'
        if port:
            if port in key or port in port_name:
                records.append([key, values, port_name])
        else:
            records.append([key, values, port_name])


    if '-' in sort:
        index = xtimes.index(sort.split('-'))
        function = lambda items, index=index: items[index]
    elif sort == 'max':
        function = max
    elif sort == 'median':
        function = median
    elif sort == 'sum':
        function = sum
    records.sort(key=lambda x: function(x[1]), reverse=True)

    try:
        quantity = int(quantity)
        records = records[:quantity]
    except:
        pass

    integers = integers['p'] if integers else {}
    integer = integers.get(counter, None)


    if counter is None:
        counter = []

    data = {
        'datestring': datestring,
        'xtimes': xtimes,
        'rows': records,
        'ptype': 'port',
        'counters': sort_counters(cdicts.keys()),
        'counter': counter,
        'integer': integer,
        'sort': sort,
        'filter': port,
        'ports_quantity': quantity,
    }
    return render(request, 'bc/date.html', data)


def select_view(request):
    datestring = request.GET.get('date')
    select_ports = request.GET.getlist('ports')
    select_counters = request.GET.getlist('counters')

    if datestring is None:
        return redirect('%s?date=%s' %(request.path, datetime.now().strftime('%Y-%m-%d')))

    xtimes = []
    records = []
    ports = []

    for obj in Portshow.objects.all():
        ports.append(['%s %s' %(obj.Switch, obj.portIndex), obj.portName])

    if select_ports and select_counters:

        xtimes = XTimes.objects.get(date=datestring).values
        integers = Integers.objects.get(date=datestring).values
        cdicts = CDicts.objects.get(date=datestring).values

        for counter in select_counters:
            integer = integers['p'].get(counter, '')
            counter_ports = cdicts.get(counter, {})
            port_values = []
            for port in select_ports:

                sw, po = port.split()
                ports_objs = Portshow.objects.filter(Switch=sw, portIndex=po)
                if ports_objs:
                    port_name = ports_objs[0].portName
                else:
                    port_name = '?'

                values = counter_ports.get(port, [])
                port_values.append([[port, port_name], values])

            if sum([sum(x[1]) for x in port_values]):
                records.append([counter, port_values, integer])

    data = {
        'datestring': datestring,
        'ports': ports,
        'counters': COUNTERS,
        'xtimes': xtimes,
        'select_ports': select_ports,
        'select_counters': select_counters,
        'records': records,
    }
    return render(request, 'bc/select.html', data)
