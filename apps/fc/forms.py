from django.forms import ModelForm
from .models import Change

class ChangeForm(ModelForm):

     class Meta:
         model = Change
         fields = ['id', 'Note']
