from django.conf.urls import url
from django.views.generic import ListView
from . import views
from .models import *

app_name = 'Wettbewerbe'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^Personen/$', 
        views.ListeZuKategorie.as_view(model=Person), 
        name='liste_personen'),
    url(r'^Veranstaltungen/$', 
        views.ListeZuKategorie.as_view(model=Veranstaltung), 
        name='liste_veranstaltungen'),
    url(r'^(?P<art_kategorie>[\w-]+)/$', 
        views.ListeZuKategorie.as_view(model=ArtKategorie), 
        name='liste_kategorie'),

    url(r'^([\w-]+)/([\w-]+)/$', 
        views.ebene1, 
        name='spam'),
]
