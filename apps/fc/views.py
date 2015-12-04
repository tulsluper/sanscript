from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import json
from datetime import datetime, timedelta
from .models import *
from .forms import *
from apps.sa.defs import sfilter, stable


def home(request):
    return redirect('/fc/switches/')


def stat(request):
    node1 = request.GET.get('node1')
    node2 = request.GET.get('node2')
    if node1 and node2:
        try:
            treads = Path.objects.get(Node1=node1, Node2=node2).Treads
        except:
            treads = []
        ports = set()
        for tread in treads:
            for node in tread:
                if ' ' in node:
                    ports.add(node)
        
        url = '/bc/select/?date={}'.format(str(datetime.now().date()))
        for port in ports:
            url += '&ports={}'.format(port.replace(' ', '+'))
        for counter in ['Error', 'TxElements', 'RxElements','BBCreditZero']:
            url += '&counters={}'.format(counter)
        return redirect(url)
    return redirect('/fc/paths/')


@csrf_protect
def paths(request):

    def get_zoned_swports(swport):
        '''
        form list of swports
        that are zoned with <swport>, swport is 'switch port'; 
        return [['switch port', ['alias', ...]], ...]
        '''
        zswports = PortRelation.objects.get(Port=swport).Relation
        for num, zswport in enumerate(zswports):
            aliases = SwportAlias.objects.get(Swport=zswport).Aliases
            zswports[num] = [zswport, aliases]
        return zswports

    def form_same_ports(sw, swport):
        '''
        form list of ports on switch <sw>
        that are zoned with <swport>, swport is 'switch port';
        return [[port, ['alias', ...]], ...]
        '''
        outlist = []
        for zswport, zaliases in get_zoned_swports(swport):
            zsw, zport = zswport.split()
            if zsw == sw:
                outlist.append([int(zport), zaliases])
        return sorted(outlist)


    node1 = request.GET.get('node1')
    node2 = request.GET.get('node2')
    if request.is_ajax(): 
        node1 = request.POST.get('node1')
    ports1 = SwportAlias.objects.all()
    ports2 = get_zoned_swports(node1) if node1 else []
    if request.is_ajax():
        return HttpResponse(json.dumps(ports2))

    nodes = None
    links = None
    internal_links = []
    maxports = 0
    same_ports = {}

    if node1 and node2:

        try:
            path = Path.objects.get(Node1=node1, Node2=node2)
        except:
            data = {
                'ports': ports1,
                'ports2': ports2,
                'node1': node1,
                'node2': node2,
                'warning': 'path not found',
            }
            return render(request, 'fc/path.html', data)

        nodes = path.Nodes
        links = path.Links

        same_ports['left'] = form_same_ports(node1.split()[0], node2)
        same_ports['right'] = form_same_ports(node2.split()[0], node1)

        maxports = max([len(v2) for v1 in nodes for v2 in v1[1].values()])
        maxports = max(maxports, len(same_ports['left']), len(same_ports['right']))

        internal = {}
        for link in links:
            TrunkId = link['TrunkId']
            sw = link['node1'].split('_')[0]
            if TrunkId:
                key = '%s %s' %(sw, TrunkId)
                if not key in internal:
                    internal[key] = {
                        'Left': {'Master': '', 'Slave':[], 'Position': 'Left'},
                        'Right': {'Master': '', 'Slave':[], 'Position': 'Right'}
                    }
                if link['Master']:
                    internal[key]['Left']['Master'] = link['node1']
                    internal[key]['Right']['Master'] = link['node2']
                else:
                    internal[key]['Left']['Slave'].append(link['node1'])
                    internal[key]['Right']['Slave'].append(link['node2'])

        for record in internal.values():
            for key, value in record.items():
                internal_links.append(value)

    data = {
        'ports': ports1,
        'ports2': ports2,
        'node1': node1,
        'node2': node2,
        'nodes': nodes,
        'links': links,
        'height': (maxports+1)*40+16,
        'internal': internal_links,
        'same_ports': same_ports,
        'bcounters': True,
        'js_jsPlumb': True,
    }
    return render(request, 'fc/path.html', data)


def switches(request):
    objs = sfilter(SwitchCommon, request)
    cols, rows = stable(SwitchCommon, objs)
    data = {
        'cols': cols,
        'rows': rows,
    }
    return render(request, 'table.html', data)


def ports(request):
    objs = sfilter(PortCommon, request)
    cols, rows = stable(PortCommon, objs)
    for row in rows:
        for index, cell in enumerate(row):
            if type(cell) == list:
                row[index] = '<br>'.join(cell)
    data = {
        'cols': cols,
        'rows': rows,
    }
    return render(request, 'table.html', data)


def fix_cell(cell):
    new_cell = []
    for key in sorted(cell.keys()):
        value = cell[key]
        if type(value) == bool:
            color = 'green' if value else 'red'
            new_cell.append('<span style="color:%s">%s</span>' %(color, key))
        elif type(value) == dict:
            new_cell.append('%s %s' %(key, fix_cell(value)))
    new_cell = '<br>'.join(new_cell)
    return new_cell



def aliases(request):
    objs = sfilter(AliasStatus, request)
    cols, rows = stable(AliasStatus, objs)
    for row in rows:
        for index, cell in enumerate(row):
            if type(cell) == dict:
                row[index] = fix_cell(cell)
    data = {
        'cols': cols,
        'rows': rows,
    }
    return render(request, 'table.html', data)


def zones(request):
    objs = sfilter(ZoneStatus, request)
    cols, rows = stable(ZoneStatus, objs)
    for row in rows:
        for index, cell in enumerate(row):
            if type(cell) == dict:
                row[index] = fix_cell(cell)
    data = {
        'cols': cols,
        'rows': rows,
    }
    return render(request, 'table.html', data)


@csrf_protect
def changes(request):
    field_latest = 'id'
    if request.is_ajax():
        data = {}
        try:
            if Change.objects.latest(field_latest).id != int(request.POST.get('last_obj_id')):
                data = {'refresh': True}
        except:
            pass
        return HttpResponse(json.dumps(data), content_type='application/json')

    objs = sfilter(Change, request)
    last_obj_id = objs.latest(field_latest).id if objs else None

    data = {
        'objs': objs,
        'last_obj_id': last_obj_id,
    }
    return render(request, 'fc/changes.html', data)


@csrf_protect
def change_acknowledge(request): 
    id = request.GET.get('id')
    instance = Change.objects.get(id=id)
    form = ChangeForm(request.POST or None, instance=instance)
    if form.is_valid():
          instance = form.save(commit=False)
          instance.Acknowledged = True
          instance.save()
          return redirect('/fc/changes/')
    data = {
        'instance': instance,
        'form': form,
    }
    return render(request, 'fc/change_acknowledge.html', data)


def portlog(request):

    if request.GET.get('dt') is None:
        try:
            dt10 = str(Portlog.objects.last().dt)[:16]
        except:
            dt10 = '2016-01-01 00:00'
        return redirect('/fc/portlog/?dt={}'.format(dt10))

    objs = sfilter(Portlog, request)
    cols, _ = stable(Portlog, [])

    if len(objs) > 10000:
        data = {
            'cols': cols,
            'warning': 'More than 10000 records. Please refine select.',
        }
        return render(request, 'fc/portlog.html', data)

    if not objs:
        data = {
            'cols': cols,
            'warning': 'No data for this select. Please refine select.',
        }
    
        return render(request, 'fc/portlog.html', data)

    cols, rows = stable(Portlog, objs)


    events = {}
    swports = {}
    for obj in objs:
        event = '{} {}'.format(obj.task, obj.event)
        swport = '{} {}'.format(obj.switch, obj.port)
        if not event in events:
            events[event] = 0
        events[event] += 1
        if not swport in swports:
            swports[swport] = 0
        swports[swport] += 1


    matrix = {}
    dts = set()
    for obj in objs:
        swport = '{} {}'.format(obj.switch, obj.port)
        if not swport in matrix:
            matrix[swport] = set()
        dt = obj.dt.replace(microsecond=0)
        matrix[swport].add(dt)
        dts.add(dt)
    
    period = [min(dts)+timedelta(seconds=s) for s in range((max(dts)-min(dts)).seconds+1)]
    xlist = []
    for swport, values in matrix.items():
        xlist.append([swport, ['x' if s in values else '' if s in dts else '-' for s in period]])

    secdict = {}
    for sec in period:
        minute = sec.replace(second=0)
        if not minute in secdict:
            secdict[minute] = []
        secdict[minute].append(sec.second)
    seclist = [[minute, secdict[minute]] for minute in sorted(secdict.keys())]

    for swport in swports.copy():
        try:
            switch, index = swport.split()
            portname = PortCommon.objects.get(Switch=switch, Index=index).portName
            swports['{} {}'.format(swport, portname)] = swports.pop(swport)
        except:
            pass

    data = {
        'cols': cols,
        'rows': rows,
        'xlist': xlist,
        'minutes': seclist,
        'events': sorted(list(events.items()), key=itemgetter(1), reverse=True),
        'swports': sorted(list(swports.items()), key=itemgetter(1), reverse=True),
    }
    
    return render(request, 'fc/portlog.html', data)

from operator import itemgetter
def fabriclog(request):
    if request.GET.get('dt') is None:
        try:
            dt10 = str(Portlog.objects.last().dt)[:7]
        except:
            dt10 = str(datetime.now())[:7]
        return redirect('/fc/fabriclog/?dt={}'.format(dt10))

    objs = sfilter(Fabriclog, request)
    cols, _ = stable(Portlog, [])

    if not objs:
        data = {
            'cols': cols,
            'warning': 'No data for this select. Please refine select.',
        }

    cols, rows = stable(Fabriclog, objs)

    actions = {}
    swports = {}
    for obj in objs:
        action = obj.action.split(';')[0]
        swport = '{} {}'.format(obj.switch, obj.Port)
        if not action in actions:
            actions[action] = 0
        actions[action] += 1
        if not swport in swports:
            swports[swport] = 0
        swports[swport] += 1
    
    for swport in swports.copy():
        try:
            switch, index = swport.split()
            portname = PortCommon.objects.get(Switch=switch, Index=index).portName
            swports['{} {}'.format(swport, portname)] = swports.pop(swport)
        except:
            pass

    data = {
        'cols': cols,
        'rows': rows,
        'actions': sorted(list(actions.items()), key=itemgetter(1), reverse=True),
        'swports': sorted(list(swports.items()), key=itemgetter(1), reverse=True),
    }
    return render(request, 'fc/fabriclog.html', data)
