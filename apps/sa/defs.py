"""
Functions for sa and other project applications.
"""


from django.forms.models import modelformset_factory
from django.forms import PasswordInput
from operator import or_, and_
from django.db.models import Q
from django.db.models import Sum
from decimal import Decimal


def create_formset(Model):
    """
    | Creates formset for model.

    Args:
        model (django.db.models.base.ModelBase): Model instance.

    Returns:
        django.forms.formsets.BaseFormSet: Formset for model.
    """
    FormSet = modelformset_factory(
        Model,
        exclude=(),
        can_delete=True,
        widgets = {
            'password': PasswordInput(),
        }
    )
    return FormSet


def sfilter(model, request):
    """
    | Filters all model objects by fields values in request.GET.
    | Allows using '&&' and '||' in filter.
    Args:
        model (django.db.models.base.ModelBase): Model instance.
        request (django.core.handlers.wsgi.WSGIRequest): Http request.

    Returns:
        django.db.models.query.QuerySet: Set of model objects.
    """

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

    def xxx_value(key, value, query):
                value=value.strip()
                if value[:2] == '[[' and value[-2:] == ']]':
                    value = value[2:-2].replace(',','')
                    value = '["'+'","'.join(value.split())+'"]'
                    key = '{}__contains'.format(key)
                elif value[0] == '[' and value[-1] == ']':
                    value = value[1:-1]
                else:
                    key = '{}__contains'.format(key)

                if '&&' in value or '||' in value:
                    query.add(
                        set_op(or_, key, [set_op(and_, key, z) for z in [[ i.strip() for i in x.split('&&')] for x in value.split('||')]]), Q.AND)
                else:
                    query.add(Q((key, value)), Q.AND)
                return query



#    limit = 3000
    objects = []
    if ''.join(list(request.GET.values())) != '':
        query = Q()
        ex_query = Q()
        for key, value in request.GET.items():
            key = key.replace(' ', '_')
            if value:
                value = value.replace('+', ' ')
                ex_value = None
                if '!' in value:
                    value, ex_value = value.split('!', 1)

                query = xxx_value(key, value, query)

                if ex_value:
                    ex_query = xxx_value(key, ex_value, ex_query)


        objects = model.objects.filter(query)#.exclude(ex_query)#[:limit]
        objects = objects.exclude(ex_query)
                    
    else:
        objects = model.objects.all()#[:limit]
    return objects


def stable(model, objects, fields=None):
    """
    | Converts model objects to list of lists of fields values.
    | If fields are not specified gets all fields except 'Id'.
    | If value is ``None`` or field is 'password' replaces value to ``''``.

    Args:
        model (django.db.models.base.ModelBase): Model instance.
        objects (django.db.models.query.QuerySet): Set of model objects.
        fields (list): Fields names. Defaults to None.

    Returns:
        list, list: Fields names, fields values.
    """

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

            if type(value) == Decimal:
                value = '<span class="decimal">{}</span>'.format(value)
            elif type(value) == list:
                value = ', '.join(value)

            row.append(value)
        rows.append(row)
    return fields, rows


def sum_by_field(model, objects, fields=None):
    """
    | Calculates sums of fields values of objects by each field.
    | If fields are not specified gets all fields except 'Id'.

    Args:
        model (django.db.models.base.ModelBase): Model instance.
        objects (django.db.models.query.QuerySet): Set of model objects.
        fields (list): Fields names. Defaults to None.

    Returns:
        dict: Sums of fields values.
    """

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


def sum_by_field_to_list(model, objects, fields=None):
    """
    | Calculates sums of fields values of objects by each field.
    | If fields are not specified gets all fields except 'Id'.

    Args:
        model (django.db.models.base.ModelBase): Model instance.
        objects (django.db.models.query.QuerySet): Set of model objects.
        fields (list): Fields names. Defaults to None.

    Returns:
        dict: Sums of fields values.
    """

    row = []

    table_fields = [f.name for f in model._meta.fields][1:]
    row = ['' for _ in table_fields]
    if fields is None:
        fields = table_fields
    for field in fields:
        try:
            value = list(objects.aggregate(Sum(field)).values())[0]
            value = '<span class="decimal">{}</span>'.format(value)
        except:
            value = None
        row[table_fields.index(field)] = value
    return row


