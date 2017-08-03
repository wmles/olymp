from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from . import models


class IndexView(ListView):
    """ zeigt die Startseite an :) """
    template_name = 'Ehemalige/index.html'
    model = models.Ehemaliger
    context_object_name = 'ehemalige'

#@login_required
class EintragenView(CreateView):
    """ Erstellt einen neuen Ehemaligen-Eintrag """
    template_name = 'Ehemalige/eintragen.html'
    model = models.Ehemaliger
    fields = ['bezeichnung', 'lebenslauf', 'ort', 'taetigkeit']
    
    def get_success_url(self, *args, **kwargs):
        return reverse('Ehemalige:index')
        
    def form_valid(self, form):
        """ Setzt den erstellenden Nutzer.
        form.instance wurde vor dem Aufrufen dieser Funktion erstellt, nur 
        noch nicht in die db geschrieben (wär ja auch nicht valide); vorher 
        müssen die null=False-Felder gesetzt werden """
        form.instance.nutzer_id = self.request.user.pk
        form.instance.save()
        return super().form_valid(form)
    
