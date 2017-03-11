"""
Die Datenmodelle für die Wettbewerbsdatenbank

 - Zentral ist Teilnahme von Personen an Veranstaltungen
 - Veranstaltung kann Wettbewerbsrunde oder Seminar sein
 - Parallel gibt es Beschreibungen von Wettbewerben, sinnvoll gruppiert
 - Verknüpfungen zwischen Veranstaltungen sind indirekt über Kategorien
"""

from django.db import models

class Grundklasse(models.Model):
    bezeichnung = models.CharField(max_length=30)
        
    datum_erstellt = models.DateTimeField(
        auto_now_add=True,
        editable=False)

    def __str__(self):
        return str(self.bezeichnung)

    class Meta:
        abstract = True
        ordering = ["bezeichnung"]

class ArtTeilnahme(Grundklasse):
    """ Bezeichnung der Art: xy.Preis, Organisator, etc """
    pass

class ArtVeranstaltung(Grundklasse):
    """ Bezeichnung der Art: Seminar, Olympiaderunde, etc 
    
    Bestimmt darüber, welche Teilnahmearten es gibt
    """
    teilnahmearten = models.ManyToManyField(ArtTeilnahme) 

class Veranstaltung(Grundklasse):
    """ Eine konkrete Veranstaltung: Seminar, Wettbewerbsrunde, etc. """
    art = models.ForeignKey(ArtVeranstaltung)
    gehoert_zu = models.ForeignKey(
        "WettbewerbsKategorie", 
        blank=True, null=True)

class Person(Grundklasse):
    """ Alle Attribute einer Person, später: Verknüpfung zu User """
    veranstaltungen = models.ManyToManyField(Veranstaltung, through='Teilnahme')

class Teilnahme(Grundklasse):
    """ Wie konkret hat die Person an der Veranstaltung teilgenommen """
    person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True)
    veranstaltung = models.ForeignKey(
        Veranstaltung,
        on_delete=models.SET_NULL,
        null=True)
    art = models.ForeignKey(
        ArtTeilnahme,
        on_delete=models.SET_NULL,
        null=True)

    def __str__(self):
        return '{} - {}'.format(self.person, self.veranstaltung)


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

class ArtKategorie(Grundklasse):
    """ Die zur Auswahl stehenden Arten: Fachbereich, Wettbewerbsrunde """
    plural = models.CharField(max_length=30, null=True)


class Unterseite(Grundklasse): # ist das eine Sackgasse?
    """ Der Grundbaustein der Logik der Anzeige; abseits restlicher Daten
    """
    gehoert_zu = models.ForeignKey(
        'Unterseite', 
        null=True) # für die eine top-Level-Seite
    template_name = models.CharField(
        max_length=40, 
        null=True, blank=True)
    
