from django.db import models


class BaseItem(models.Model):
    table = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name
    class Meta:
        abstract = True
        ordering = ['id']


class ObjectItem(BaseItem):
    pass


class TriggerItem(BaseItem):
    pass


class Rule(models.Model):
    operators = (
        ('and', 'and'),
        ('or', 'or'),
    )
    name = models.CharField(max_length=100)
    object_item = models.ForeignKey(ObjectItem, blank=True, null=True)
    object_terms_oper = models.CharField(max_length=3, choices=operators, default='and')
    trigger_item = models.ForeignKey(TriggerItem, blank=True, null=True)
    trigger_terms_oper = models.CharField(max_length=3, choices=operators, default='and')
    severity = models.PositiveSmallIntegerField(choices=(
        (0, 'Emergency'),
        (1, 'Alert'),
        (2, 'Critical'),
        (3, 'Error'),
        (4, 'Warning'),
        (5, 'Notice'),
        (6, 'Informational'),
        (7, 'Debug'),
    ), default=6)


class BaseTerm(models.Model):
    field = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    rule = models.ForeignKey(Rule, null=True)
    def __str__(self):
        return self.field
    class Meta:
        abstract = True
        ordering = ['id']

class ObjectTerm(BaseTerm):
    pass

class TriggerTerm(BaseTerm):
    pass


class Action(models.Model):
    method = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
    rule = models.ForeignKey(Rule, null=True)

