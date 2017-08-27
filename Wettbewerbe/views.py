import sys
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import *

class IndexView(ListView):
    """ zeigt die Startseite an :) """
    def get_queryset(self):
        return ArtKategorie.objects.all()
    
    template_name = 'Wettbewerbe/index.html'
    context_object_name = 'kategorien'

class ListeKategorienZuArt(ListView):
    """ Stellt Liste der Objekte einer WettbewerbsKategorie (wobei Person 
    und Veranstaltung hier nicht ganz korrekt als Kategorie mitzählen) dar.

    Der view sucht eine Liste der entsprechenden Objekte, gibt die Liste und 
    den Namen für die Überschrift zurück """
    template_name = 'Wettbewerbe/liste_kategorien.html'
    context_object_name = 'kategorien'
    
    def get_queryset(self):
        """ bekommt von der urls.py einen kwarg model übergeben, damit alle 
        Listen in einem view bearbeitet werden können (eleganter?) """
        if self.model == ArtKategorie:
            self.art = get_object_or_404(
                ArtKategorie, 
                plural=self.kwargs['plural_kategorie'].capitalize())
            return WettbewerbsKategorie.objects.filter(art_kategorie=self.art)
        elif self.model == Person:
            return Person.objects.all()
        elif self.model == Veranstaltung:
            return Veranstaltung.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
    model = WettbewerbsKategorie


# *** views zum Eintragen ***

def eintragen_mich_zu_veranstaltung(request, slug):
    """ prüft, ob eine Person zum Nutzer existiert, und leitet je nachdem
    an EintragenTeilnahmeMich oder EintragenPersonMich weiter """
    veranstaltung = get_object_or_404(Veranstaltung, slug=slug)
    profil = request.user.my_profile
    if hasattr(profil, 'person') and isinstance(profil.person, Person):
        person = profil.person
    elif request.user.first_name and request.user.last_name:
        # quick and dirty Person erstellen
        person = Person.objects.create(
            bezeichnung='{} {}'.format(
                request.user.first_name, request.user.last_name),
            nutzer = profil,
        )
    else:
        return EintragenPersonMich.as_view()(request, slug=slug)

    return EintragenTeilnahmeMich.as_view()(request, slug=slug, person=person)

    
class EintragenTeilnahmeMich(CreateView):
    template_name = 'Wettbewerbe/formular_mich_eintragen.html'
    model = Teilnahme
    fields = ['art']
    
    def get_success_url(self):
        return reverse(
            'Wettbewerbe:eine_veranstaltung', 
            kwargs={'slug': self.kwargs['slug']})
         
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        veranstaltung = get_object_or_404(Veranstaltung, slug=self.kwargs['slug'])
        person = self.kwargs['person']
        instanz = Teilnahme(
            veranstaltung=veranstaltung, 
            person=person)
        kwargs.update([('instance', instanz)])
        return kwargs
    
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['art'].queryset = \
            form.instance.veranstaltung.art.teilnahmearten.all()
        return form


class EintragenPersonMich(CreateView):
    """ Trägt Vorname und Nachname als Daten vom Nutzer ein und erstellt
    eine Person mit dieser Bezeichnung """
    template_name = 'Wettbewerbe/formular_person_eintragen.html'
    model = get_user_model()
    fields = ['first_name', 'last_name']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        nutzer = self.request.user
        kwargs.update([('instance', nutzer)])
        return kwargs
    
    def get_success_url(self):
        return reverse('Wettbewerbe:eintragen_veranstaltung_mich', 
            kwargs={'slug': self.kwargs['slug']})
    
    def form_valid(self, form):
        """ wird aufgerufen, wenn Eingaben ok sind; soll den Nutzer (steht
        in form.instance) speichern und außerdem eine Person mit diesem 
        Namen erstellen und dem Nutzerprofil verknüpfen """
        name = '{} {}'.format(
            form.instance.first_name, form.instance.last_name)
        person = Person.objects.create(
            bezeichnung=name, 
            nutzer=form.instance.my_profile)
        self.object = form.save()
        return super(EintragenPersonMich, self).form_valid(form)

        
@login_required
def teilnahme_eintragen(request, model='Person', slug=''):
    """ der view sendet ein Formular zur Erstellung einer Teilnahme an 
    das entsprechende Template oder nimmt POST-Daten zum Speichern an """    
    if not request.user.username == 'admin':
        return HttpResponseRedirect('/admin/')

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


