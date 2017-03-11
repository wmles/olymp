import sys
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from .models import *

class IndexView(ListView):
    """ zeigt die Startseite an :) """
    def get_queryset(self):
        startseite = get_object_or_404(Unterseite, gehoert_zu=None)
        return Unterseite.objects.filter(gehoert_zu=startseite)
    
    template_name = 'Wettbewerbe/index.html'
    context_object_name = 'unterseiten'

class ListeZuKategorie(ListView):
    """ Stellt Liste der Objekte einer Kategorie - Person/Fachbereich/etc dar

    Der view sucht eine Liste der entsprechenden Objekte, gibt die Liste und 
    den Namen für die Überschrift zurück """
    template_name = 'Wettbewerbe/ListeZuKategorie.html'
    context_object_name = 'kategorien'
    
    def get_queryset(self):
        if self.model == ArtKategorie:
            self.art = get_object_or_404(
                ArtKategorie, 
                plural=self.kwargs['art_kategorie'])
            return WettbewerbsKategorie.objects.filter(art_kategorie=self.art)
        elif self.model == Person:
            return Person.objects.all()
        elif self.model == Veranstaltung:
            return Veranstaltung.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(ListeZuKategorie, self).get_context_data(**kwargs)
        if self.model == ArtKategorie:
            context['art'] = self.art.plural
        else:
            context['art'] = self.model.__name__ + 'en'
        return context

### ?        
def ebene1(request, *args):
    """ vorläufige Funktion, um Seiten der Tiefe 1 zu bearbeiten """
    if not len(args) == 1:
        sys.exit('view "ebene1" wurde mit %s Argumenten '
            'aufgerufen, brauche 1' % len(args))
    slug = args[0]
    get_object_or_404(Unterseite, bezeichnung=slug) # Achtung, ändern!!!
    view = ListeZuKategorie()
    #view.args = args
    return view.dispatch(request, *args)


