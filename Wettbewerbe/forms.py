from django import forms
from .models import *

class TeilnahmeEintragenFormular(forms.ModelForm):
    class Meta:
        model = Teilnahme
        fields = ['person', 'nur_name', 'veranstaltung', 'art']
        # widgets = {'land': CountrySelectWidget()}
