from django import forms
from .models import *

class TeilnahmeEintragenFormular(forms.ModelForm):
    class Meta:
        model = Zeile
        fields = ['autor_name', 'text']
