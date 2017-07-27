from django.shortcuts import render
from django.views.generic.edit import CreateView
from django import forms as django_forms
from . import models
import ipdb

# Create your views here.

class ZeigenUndEintragen(CreateView):
    """ zeigt die bisher einzige Liste an """
    template_name = 'Notizen/index.html'
    model = models.Zeile
    fields = ['autor', 'autor_name', 'text']
    context_object_name = 'liste'

    def render_to_response(self, context, **kwargs):
        """ Gibt eine Instanz von TemplateResponse zurück
        ich übergebe der zusätzlich eine Liste aller Zeilen; später nur die 
        zugehörigen zu einer models.Liste, außerdem wird die Eingabe des Autors
        versteckt, da die automatisch passiert """
        response = super().render_to_response(context, **kwargs)
        # übergebe Liste von Zeilen
        response.context_data.update([
            ('liste', models.Zeile.objects.all())
        ])
        # form.autor verstecken, der wird in self.form_valid automatisch gesetzt
        form = response.context_data['form']
        form.fields['autor'].widget = django_forms.HiddenInput()
        ipdb.set_trace()
        form.fields['autor'] = self.request.user
        return response
    
