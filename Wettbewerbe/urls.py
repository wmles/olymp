from django.conf.urls import url, include
from django.views.generic import ListView
from . import views
from .models import *

app_name = 'Wettbewerbe'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    # alles was mit person beginnt: liste, detail, formular
    url(r'^personen/$', 
        views.ListeKategorienZuArt.as_view(
            model=Person,
            template_name = 'Wettbewerbe/liste_personen.html'), 
        name='liste_personen'),
    url(r'^person/', include([ 
        url(r'^(?P<slug>[\w-]+)/veranstaltung_eintragen/$', 
            views.teilnahme_eintragen,
            {'model': 'Person'}, 
            name='eine_person_formular'),
        url(r'^(?P<slug>[\w-]+)/$', 
            views.EinePerson.as_view(), 
            name='eine_person'),
    ])),

    # alles was mit veranstaltung beginnt: liste, detail, formular
    url(r'^veranstaltungen/$', 
        views.ListeKategorienZuArt.as_view(
            model=Veranstaltung, 
            template_name = 'Wettbewerbe/liste_veranstaltungen.html'), 
        name='liste_veranstaltungen'),
    url(r'^veranstaltung/', include([ 
        url(r'^(?P<slug>[\w-]+)/person_eintragen/$', # prüft, ob es admin ist
            views.teilnahme_eintragen,
            {'model': 'Veranstaltung'}, 
            name='eintragen_zu_veranstaltung'),
        url(r'^(?P<slug>[\w-]+)/mich_eintragen/$', # zum Nutzer zugehörige Person eintragen
            views.eintragen_mich_zu_veranstaltung,
            name='eintragen_veranstaltung_mich'),
        url(r'^(?P<slug>[\w-]+)/$', 
            views.EineVeranstaltung.as_view(), 
            name='eine_veranstaltung'),
    ])),

    # Kategorien: Listen unter <art.plural>/, Detail <art.slug>/<kat.slug>/
    url(r'^(?P<art_kategorie>[\w-]+)/(?P<slug>[\w-]+)/$', 
        views.EineKategorie.as_view(), 
        name='eine_kategorie'),
    url(r'^(?P<plural_kategorie>[\w-]+)/$',  
        views.ListeKategorienZuArt.as_view(model=ArtKategorie), 
        name='liste_kategorie'),

    
    # wird hoffentlich nie erreicht, wäre nur bei 3.Ebene-Verschachtelung
    url(r'^([\w-]+)/(.+)', 
        views.rest, 
        name='spam'),
]
