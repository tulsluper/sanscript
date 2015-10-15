from django.db import models


class AppDataLastUpdate(models.Model):
    appname = models.CharField(max_length=16)
    datetime = models.DateTimeField(auto_now_add=True)
