from django import forms
from .models import *
from django.apps import apps
from django.forms.models import modelformset_factory


tables = [('', '')]
for app in apps.get_app_configs():
    if app.name.startswith('apps.'):
        for model in app.models:
            app_table = '{} {}'.format(app.label, model)
            tables.append((app_table, app_table))


class ObjectItemForm(forms.ModelForm):
    class Meta:
        model = ObjectItem
        exclude = ()
    table = forms.ChoiceField(choices=tables)


class TriggerItemForm(forms.ModelForm):
    class Meta:
        model = TriggerItem
        exclude = ()


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        exclude = ()
        widgets = {
            'object_terms_oper': forms.RadioSelect(),
            'trigger_terms_oper': forms.RadioSelect(),
        }


class RuleObjectItemForm(forms.Form):
    name = forms.ChoiceField(
        choices = [('', '')] +
        [(o.id, o.name) for o in ObjectItem.objects.all()]
    )

action_methods = [
    ('', '---------'),
    ('email', 'send email'),
    ('log', 'write log'),
]
ActionFormSet = modelformset_factory(
    Action,
    can_delete=True,
    exclude=('rule',),
    widgets={
        'method': forms.Select(choices=action_methods),
    }
)


