from django.db import models
from jsonfield import JSONField


# ==============================================================================


class SwitchConnection(models.Model):
    name = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=256, unique=True)
    enabled = models.BooleanField(default=True)
    order = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['order', 'pk']


class CounterOid(models.Model):
    number = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=64, unique=True)
    enabled = models.BooleanField(default=True)
    order = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['order', 'pk']

# ==============================================================================

class XTimes(models.Model):
    date = models.DateField()
    values = JSONField()

class Deltas(models.Model):
    date = models.DateField()
    values = JSONField()

class CDicts(models.Model):
    date = models.DateField()
    values = JSONField()

class PDicts(models.Model):
    date = models.DateField()
    values = JSONField()

class SDicts(models.Model):
    date = models.DateField()
    values = JSONField()

class Integers(models.Model):
    date = models.DateField()
    values = JSONField()

class PortConfig(models.Model):
    switchname = models.CharField(max_length=30)
    portindex = models.IntegerField()
    portname = models.CharField(max_length=60)
    porttype = models.IntegerField()

