import sys
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import *

class IndexView(ListView):
    """ zeigt die Startseite an :) """
    def get_queryset(self):
        return ArtKategorie.objects.all()
    
    template_name = 'Wettbewerbe/index.html'
    context_object_name = 'kategorien'

class ListeZuKategorie(ListView):
    """ Stellt Liste der Objekte einer WettbewerbsKategorie (wobei Person 
    und Fachbereich hier nicht ganz korrekt als Kategorie mitzählen) dar.

    Der view sucht eine Liste der entsprechenden Objekte, gibt die Liste und 
    den Namen für die Überschrift zurück """
    template_name = 'Wettbewerbe/liste_kategorien.html'
    context_object_name = 'kategorien'
    
    def get_queryset(self):
        if self.model == ArtKategorie:
            self.art = get_object_or_404(
                ArtKategorie, 
                slug=self.kwargs['art_kategorie'])
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
            context['art'] = self.model._meta.verbose_name_plural
        return context

class EinePerson(DetailView):
    template_name = 'Wettbewerbe/eine_person.html'
    context_object_name = 'person'
    model = Person

class EineVeranstaltung(DetailView):
    template_name = 'Wettbewerbe/eine_veranstaltung.html'
    context_object_name = 'v'
    model = Veranstaltung
    
class EineKategorie(DetailView):
    template_name = 'Wettbewerbe/eine_kategorie.html'
    context_object_name = 'kategorie'


from .forms import TeilnahmeEintragenFormular

@login_required
def teilnahme_eintragen(request, model='Person', slug=''):
    """ der view sendet ein Formular zur Erstellung einer Teilnahme an 
    das entsprechende Template oder nimmt POST-Daten zum Speichern an """    
    # falls POST von hier, werden Daten verarbeitet:
    if request.method=='POST':
        # eine form erstellen, insb. um sie im Fehlerfall zu nutzen:
        formular = TeilnahmeEintragenFormular(request.POST)
        # und falls alle Eingaben gültig sind, Daten verarbeiten: 
        if formular.is_valid():
            # redirect to a new URL:
            teilnahme = formular.save()
            return HttpResponseRedirect('/thanks/')
            
    else:
        # falls GET (v.a. nicht POST), erstelle neues Formular
        # wir brauchen die übergebenen Argumente der Funktion um sie
        # vorauszufüllen. Achtung hack
        Model = globals()[model]
        instanz = get_object_or_404(Model, slug=slug) 
        formular = TeilnahmeEintragenFormular(initial={model.lower(): instanz})

    return render(
            request, 
            'Wettbewerbe/formular_teilnahme_eintragen.html', 
            {'formular': formular}
        )


### ?        
def rest(request, *args):
    """ vorläufige Funktion, um restliche Seiten zu bearbeiten """
    if len(args) == 2:
        if args[0] == 'veranstaltungen':
            return DetailView.as_view(
                template_name='Wettbewerbe/veranstaltung.html', 
                context_object_name='v',
                model=Veranstaltung,
                )(request, slug=args[1])
        elif args[0] == 'personen':
            return HttpResponse('personen')
        else:
            return HttpResponse(' - '.join(args))


