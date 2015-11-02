from django.forms.models import modelformset_factory
from django.forms import PasswordInput
from operator import or_, and_
from django.db.models import Q
from django.db.models import Sum


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


def create_formset(Model):
    FormSet = modelformset_factory(
        Model,
        exclude=(),
        can_delete=True,
        widgets = {
            'password': PasswordInput(),
        }
    )
    return FormSet


def build_filters(request):
    filters = {}
    for key, value in request.GET.items():
        if value:
            if value[0] == '[' and value[-1] == ']':
                qtype = 'in'
                value = value[1:-1].split(',')
                value = [x.strip() for x in value]
            else:
                qtype = 'contains'
            filters['%s__%s' %(key, qtype)] = value
    return filters


def sfilter(model, request):
    
    objects = []

    def set_op(op, key, xs):
        if len(xs) == 1:
            return xs[0]
        elif len(xs) == 2:
            elm0 = xs[0] if type(xs[0]) == Q else Q((key, xs[0]))
            elm1 = xs[1] if type(xs[1]) == Q else Q((key, xs[1]))
            return op(elm0, elm1)
        else:
            elm0 = xs[0] if type(xs[0]) == Q else Q((key, xs[0]))
            return op(elm0, set_op(op, key, xs[1:]))

    if ''.join(list(request.GET.values())) != '':
        query = Q()
        for key, value in request.GET.items():
            if value:
                key = '{}__contains'.format(key)
                value = value.replace(' ', '').replace('+', '')
                if '&&' in value or '||' in value:
                    query.add(
                        set_op(or_, key, [set_op(and_, key, z) for z in [x.split('&&') for x in value.split('||')]]),
                        Q.AND)
                else:
                    query.add(Q((key, value)), Q.AND)

        print(query)
        objects = model.objects.filter(query)
                    
    else:
        objects = model.objects.all()
    return objects


def model_to_table(model, filters):
    fields = [f.name for f in model._meta.fields][1:]
    rows = []
    objs = model.objects.filter(**filters)[:5000]
    for record in objs:
        row = []
        for field in fields:
            value = getattr(record, field)
            if value is None:
                value = ''
            if field == 'password':
                value = ''
            row.append(value)
        rows.append(row)
    return fields, rows


def stable(model, objects, fields=None):
    if fields is None:
        fields = [f.name for f in model._meta.fields][1:]
    rows = []
    for record in objects:
        row = []
        for field in fields:
            value = getattr(record, field)
            if value is None:
                value = ''
            if field == 'password':
                value = ''
            row.append(value)
        rows.append(row)
    return fields, rows


def sum_by_field(model, objects, fields=None):
    if fields is None:
        fields = [f.name for f in model._meta.fields][1:]
    row = {}
    for field in fields:
        try:
            value = list(objects.aggregate(Sum(field)).values())[0]
        except:
            value = None
        row[field] = value
    return row



