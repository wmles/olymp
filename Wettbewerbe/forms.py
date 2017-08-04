from django import forms
from .models import *
import ipdb

class TeilnahmeEintragenFormular(forms.ModelForm):
    """ für den teilnahme_eintragen-view """
    class Meta:
        model = Teilnahme
        fields = ['person', 'nur_name', 'veranstaltung', 'art']
        # widgets = {'land': CountrySelectWidget()}
    

class TeilnahmeZuVeranstaltung(forms.ModelForm):
    """ Für admin
    ist aber nicht allgemein, nur im change-view von Teilnahmen sinnvoll
    Nur wenn self.instance schon eine veranstaltung gesetzt hat, werden 
    nur die Teilnahmearten, die dazu passen, angezeigt """
    class Meta:
        model = Teilnahme
        fields = ['person', 'nur_name', 'art']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['art'].queryset = \
            self.instance.veranstaltung.art.teilnahmearten.all()

