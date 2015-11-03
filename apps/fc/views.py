from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import json
from datetime import datetime
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


"""
def change_acknowledge(request):
    id = request.GET.get('id')
    try:
        obj = Change.objects.get(id=id)
    except:
        obj = None
    data = {
        'obj': obj,
    }
    return render(request, 'fc/change_acknowledge.html', data)
"""


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
