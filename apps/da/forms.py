from django.forms import ModelForm
from .models import VolumeChange

class VolumeChangeForm(ModelForm):

     class Meta:
         model = VolumeChange
         fields = ['id', 'Note']

