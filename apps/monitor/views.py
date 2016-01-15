from django.shortcuts import render, redirect
from .forms import *
from .models import *

import os
import json
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.forms.models import modelformset_factory
from .models import *
from .forms import *
from django.apps import apps
from django.db.models import Q
from operator import or_
from functools import reduce
from datetime import datetime

from django.core.mail import send_mail
from django.conf import settings


SEVERITY_NAMES = (
    'Emergency',
    'Alert',
    'Critical',
    'Error',
    'Warning',
    'Notice',
    'Informational',
    'Debug',
)

# Create your views here.
def home(request):
    return render(request, 'home.html')


def san_send_email(to_email, message):
    subject = "SANscript Monitor"
    from_email = settings.DEFAULT_FROM_EMAIL
    try:
        send_mail(subject, message, from_email, [to_email])
        success = 'success'
        message = 'successfully'
    except Exception as e:
        success = 'warning'
        message = e
    return success, message


def san_write_log(filepath), message:
    if not filepath.startswith('/'):
        filepath = os.path.join('apps/monitor/logs', filepath)
    try:
        f = open(filepath, 'a')
        f.write(message)
        f.close()
        success = 'success' 
        message = 'successfully'
    except Exception as e:
        success = 'warning'
        message = e
    return success, message


def perform_actions(actions, message):
    results = []
    for action in actions:
        method = action.method
        target = action.target
        success = 'success'
        if method == 'email':
            success, message = san_send_email(target, message)
        elif method == 'log':
            success, message = san_write_log(target, message)

        results.append({
            'method': method,
            'target': target,
            'message': message,
            'success': success,
        })
    return results

object_conditions = [
    ('', ''),
    ('gt', 'greater than'),
    ('lt', 'less than'),
    ('exact', 'exact'),
    ('iexact', 'iexact'),
    ('contains', 'contains'),
    ('startswith', 'startswith'),
    ('istartswith', 'istartswith'),
    ('endswith', 'endswith'),
    ('iendswith', 'iendswith'),
]

def create_modelformset(termmodel, fields, conditions):
    ModelFormSet = modelformset_factory(
        termmodel,
        can_delete=True,
        exclude=('rule',),
        widgets={
            'field': forms.Select(choices=fields),
            'condition': forms.Select(choices=conditions),
        }
    )
    return ModelFormSet


def get_rel_am_names(am_name):
    model = apps.get_model(*am_name.split())
    rel_am_names = [am_name]
    for field in model._meta.get_fields():
        if field.is_relation and not field.many_to_one:
            rel_am_meta = field.related_model._meta
            rel_am_names.append('{} {}'.format(rel_am_meta.app_label, rel_am_meta.model_name))
    return rel_am_names

def get_fields(appmodelname):
    app_label, model_name = appmodelname.split()
    model = apps.get_model(app_label, model_name)
    fields = [('', '---------'),]
    for field in model._meta.get_fields():
        if not field.is_relation and field.name != 'id':
            fields.append((field.name, field.name))
    return fields


def models_view(request):
    data = {
        'objectitems': ObjectItem.objects.all(),
    }
    return render(request, 'monitor/models.html', data)


def model_register(request):
    form = ObjectItemForm()
    if request.method == 'POST':
        form = ObjectItemForm(request.POST)
        if form.is_valid():
            object_item = form.save()
            trigger_item = TriggerItem(name=object_item.name, table=object_item.table)
            trigger_item.save()
            return HttpResponseRedirect('/monitor/models/')
    else:
        form = ObjectItemForm()
    data = {
        'form': form,
    }
    return render(request, 'monitor/model_form.html', data)


def model_edit(request):
    obj_id = request.GET.get('id')
    object_item = ObjectItem.objects.get(id=int(obj_id))
    trigger_item = TriggerItem.objects.get(name=object_item.name)
    if request.method == 'POST':
        form = ObjectItemForm(request.POST, instance=object_item)
        if form.is_valid():
            object_item = form.save()
            print(trigger_item.name, object_item.name)
            trigger_item.name = object_item.name
            trigger_item.table = object_item.table
            trigger_item.save()
            print(trigger_item.name, object_item.name)

            return HttpResponseRedirect('/monitor/models/')
    else:
        form = ObjectItemForm(instance=object_item)
        data = {
            'form': form,
            'model': object_item,
        }
        return render(request, 'monitor/model_form.html', data)

def model_unregister(request):
    obj_id = request.GET.get('id')
    object_item = ObjectItem.objects.get(id=int(obj_id))
    trigger_item = TriggerItem.objects.get(name=object_item.name)
    object_item.delete()
    trigger_item.delete()
    return HttpResponseRedirect('/monitor/models/')



def rules_view(request):
    data = {
        'rules': Rule.objects.all()
    }
    return render(request, 'monitor/rules.html', data)


def rule_empty(request):
    rule = Rule(name='xxx')
    rule.save()
    rule_id = rule.id
    return redirect('/monitor/rule?id={}'.format(str(rule_id)))


def rule_delete_view(request):
    rule_id = request.GET.get('id')
    rule = Rule.objects.get(id=rule_id)
    rule.delete()
    return HttpResponseRedirect('/monitor/rules/')


# ==============================================================================

def rule_check(rule):

    def filter_by_terms(model_objs, terms, operator):
        filters = {'{}__{}'.format(t.field, t.condition): t.value for t in terms}
        if operator == 'and':
            objs = model_objs.filter(**filters)
        elif operator == 'or':
            objs = model_objs.filter(reduce(or_, [Q(x) for x in filters.items()]))
        else:
            objs = []
        return objs, filters

    data = {}
    objs = None

    if rule.object_item:
        if rule.objectterm_set.count():
            objs, filters = filter_by_terms(
                apps.get_model(*rule.object_item.table.split()).objects,
                rule.objectterm_set.all(),
                rule.object_terms_oper,
            )
        else:
            objs = apps.get_model(*rule.object_item.table.split()).objects.all()
            filters = None

        data.update({
            'object_filter_terms': filters,
            'object_hits': objs.count(),
        })

    if objs and rule.trigger_item and rule.triggerterm_set.count():
        objs, filters = filter_by_terms(
            objs,
            rule.triggerterm_set.all(),
            rule.trigger_terms_oper,
        )
        data.update({
            'trigger_filter_terms': filters,
            'trigger_hits': objs.count(),
        })

    message = ''
    if objs:
        message = '{} - {} - {} - {} matches'.format(
            str(datetime.now())[:19], SEVERITY_NAMES[rule.severity], rule.name, objs.count(),
        )
        data.update({
            'check_message': message,
        })
    
 
    if objs and rule.action_set.count():
        actions = perform_actions(rule.action_set.all(), message)
        data.update({
            'actions': actions,
        })

    return data

# ==============================================================================




def rule_view(request):

    rule_id = request.GET.get('id')
    check_flag = request.GET.get('check')
    rule = Rule.objects.get(id=rule_id)

    rule_form = RuleForm(instance=rule, prefix='rule')
    if rule.object_item:
        rel_am_names = get_rel_am_names(rule.object_item.table)
        trigger_items = TriggerItem.objects.filter(table__in=rel_am_names)
        rule_form.fields['trigger_item'].queryset = trigger_items

    action_formset = ActionFormSet(queryset=Action.objects.filter(rule=rule), prefix='action')

    data = {
        'rule_id': rule_id,
        'check_flag': check_flag,
        'rule': rule,
        'rule_form': rule_form,
        'action_formset': action_formset,
    }

    ObjectTermFormSet = None
    if rule.object_item:
        fields = get_fields(rule.object_item.table)
        ObjectTermFormSet = create_modelformset(ObjectTerm, fields, object_conditions)
    TriggerTermFormSet = None
    if rule.trigger_item:
        fields = get_fields(rule.trigger_item.table)
        TriggerTermFormSet = create_modelformset(TriggerTerm, fields, object_conditions)

    formset1 = None
    formset2 = None

    if not request.POST:
        if rule.object_item:
            formset1 = ObjectTermFormSet(queryset=ObjectTerm.objects.filter(rule=rule), prefix='object')
        if rule.trigger_item:
            formset2 = TriggerTermFormSet(queryset=TriggerTerm.objects.filter(rule=rule), prefix='trigger')
        data.update({
            'formset1': formset1,
            'formset2': formset2,
        })

        if check_flag:
            data.update(rule_check(rule))

        return render(request, 'monitor/rule_form.html', data)


    if request.POST and request.is_ajax():

        item_id = request.POST.get('object_id')
        if item_id is not None:
            try:
                item = ObjectItem.objects.get(id=int(item_id))
            except:
                item = None
            rule.objectterm_set.all().delete()
            rule.object_item = item

            if not item:
                rule.trigger_item = None
                rule.triggerterm_set.all().delete()
            if item:
                rel_am_names = get_rel_am_names(rule.object_item.table)
                if len(rel_am_names) == 1:
                    if not rule.trigger_item or rel_am_names[0] != rule.trigger_item.table:
                        rule.trigger_item = TriggerItem.objects.get(table=rel_am_names[0])
                        rule.triggerterm_set.all().delete()
                elif len(rel_am_names) > 1:
                    if rule.trigger_item and rule.trigger_item.table in rel_am_names:
                        pass
                    else:
                        rule.trigger_item = None
                        rule.triggerterm_set.all().delete()
            rule.save()


        item_id = request.POST.get('trigger_id')
        if item_id is not None:
            try:
                item = TriggerItem.objects.get(id=int(item_id))
            except:
                item = None
            rule.triggerterm_set.all().delete()
            rule.trigger_item = item

        rule.save()
        return HttpResponse()


    if request.POST and not request.is_ajax():

        ruleform = RuleForm(request.POST, prefix='rule', instance=rule)
        if ruleform.is_valid():
            ruleform.save()

        formsets = []
        for name, FormSet, prefix in (
            ('formset1', ObjectTermFormSet, 'object'),
            ('formset2', TriggerTermFormSet, 'trigger'),
            ('action_formset', ActionFormSet, 'action'),
        ):
            if FormSet:
                formset = FormSet(request.POST, prefix=prefix)
                formsets.append(formset)
                data[name] = formset
            else:
                data[name] = None

        if all(formset.is_valid() for formset in formsets):
            for formset in formsets:
                instances = formset.save(commit=False)
                for obj in formset.deleted_objects:
                    obj.delete()
                for obj in instances:
                    obj.rule = rule
                    obj.save()
            return HttpResponseRedirect('/monitor/rule?id={}'.format(rule_id))
        else:
            return render(request, 'monitor/rule_form.html', data)



