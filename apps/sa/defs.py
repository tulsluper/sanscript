from django.forms.models import modelformset_factory
from django.forms import PasswordInput


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


