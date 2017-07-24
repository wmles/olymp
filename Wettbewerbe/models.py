"""
Die Datenmodelle für die Wettbewerbsdatenbank

 - Zentral ist Teilnahme von Personen an Veranstaltungen
 - Veranstaltung kann Wettbewerbsrunde oder Seminar sein
 - Parallel gibt es Beschreibungen von Wettbewerben, sinnvoll gruppiert
 - Verknüpfungen zwischen Veranstaltungen sind indirekt über Kategorien
"""

from django.db import models
from seite import settings
from Grundgeruest.models import Grundklasse, MinimalModel


class ArtTeilnahme(Grundklasse):
    """ Bezeichnung der Art: xy.Preis, Organisator, etc """
    class Meta: 
        verbose_name = 'Teilnahmeart'
        verbose_name_plural = 'Teilnahmearten'

class ArtVeranstaltung(Grundklasse):
    """ Bezeichnung der Art: Seminar, Olympiaderunde, etc 
    
    Bestimmt darüber, welche Teilnahmearten es gibt
    """
    teilnahmearten = models.ManyToManyField(ArtTeilnahme) 
    class Meta: 
        verbose_name = 'Art von Veranstaltungen'
        verbose_name_plural = 'Arten von Veranstaltungen'

class Veranstaltung(Grundklasse):
    """ Eine konkrete Veranstaltung: Seminar, Wettbewerbsrunde, etc. """
    art = models.ForeignKey(ArtVeranstaltung)
    gehoert_zu = models.ForeignKey(
        "WettbewerbsKategorie", 
        blank=True, null=True)
    class Meta: verbose_name_plural = 'Veranstaltungen'

class Person(Grundklasse):
    """ Alle Attribute einer Person, später: Verknüpfung zu User """
    veranstaltungen = models.ManyToManyField(Veranstaltung, through='Teilnahme')
    nutzer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    class Meta: verbose_name_plural = 'Personen'
    
class Teilnahme(MinimalModel):
    """ Verknüpft Person mit Veranstaltung, gehört zu einer Art """
    person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True, blank=True)
    nur_name = models.CharField( # falls Person nicht eingetragen, nur str
        max_length=100, 
        blank=True)
    veranstaltung = models.ForeignKey(
        Veranstaltung,
        on_delete=models.SET_NULL,
        null=True)
    art = models.ForeignKey(
        ArtTeilnahme,
        on_delete=models.SET_NULL,
        null=True)

    def __str__(self):
        if self.person:
            name = self.person
        else:
            name = self.nur_name
        return '{} - {}'.format(name, self.veranstaltung)
    
    def save(self):
        """ todo: hier noch Validierung einbauen; Art der Teilnahme muss 
        kompatibel sein, von der Art der Veranstaltung erlaubt ...."""
        super().save()
        
    class Meta: 
        verbose_name = 'Konkrete Teilnahme'
        verbose_name_plural = 'Konkrete Teilnahmen'


class WettbewerbsKategorie(Grundklasse):
    """ Der Grundbaustein aller Logik der Wettbewerbsstruktur
    
    Je nach art_kategorie können beliebige Objekte gemeint sein, von einer
    einzelnen Wettbewerbsrunde bis zum Fachbereich. Kategorien beziehen 
    sich aufeinander durch gehoert_zu.
    """
    art_kategorie = models.ForeignKey("ArtKategorie")
    gehoert_zu = models.ForeignKey(
        "WettbewerbsKategorie", 
        blank=True, null=True)
    beschreibung = models.TextField()
    
    def __str__(self): 
        return '{}: {}'.format(
            self.art_kategorie.bezeichnung, self.bezeichnung)

    class Meta: 
        verbose_name = 'Wettbewerbskategorie'
        verbose_name_plural = 'Wettbewerbskategorien'

class ArtKategorie(Grundklasse):
    """ Die zur Auswahl stehenden Arten: Fachbereich, Wettbewerbsrunde """
    plural = models.CharField(max_length=30, null=True)
    class Meta: verbose_name_plural = 'Arten der Wettbewerbskategorien'


class Unterseite(Grundklasse): # erstmal ohne das, ist das eine Sackgasse?
    """ Der Grundbaustein der Logik der Anzeige; abseits restlicher Daten
    """
    gehoert_zu = models.ForeignKey(
        'Unterseite', 
        null=True) # für die eine top-Level-Seite
    template_name = models.CharField(
        max_length=40, 
        null=True, blank=True)
    class Meta: verbose_name_plural = 'Unterseiten'
    
