"""
Die Datenmodelle für Notizzettel:
Zeilen sind verknüpft zu Listen (jede für eine Instanz/url)
"""

from django.db import models
from seite import settings
from Grundgeruest.models import Grundklasse, MinimalModel

import ipdb


class Liste(Grundklasse):
    """ Attribute einer Liste """
    class Meta:
        verbose_name = 'Notizzettel'
        verbose_name_plural = 'Notizzettel'

class Zeile(MinimalModel):
    """ Eine konkrete Veranstaltung: Seminar, Wettbewerbsrunde, etc. """
    liste = models.ForeignKey(Liste)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL)
    autor_name = models.CharField(max_length=30, blank=True)
    text = models.CharField(max_length=255)
    def autor_ausgeben(self):
        """ System: es wird immer der eingetragene Name angegeben; wenn der
        Autor unangemeldet war, dann mit (Gast) """
        if self.autor_id == 1: # wenn anonym
            return self.autor_name + ' (Gast)'
        else:
            return '<a href="/nutzer/%s">%s</a>' % (self.autor.username, self.autor_name)
            
    def __str__(self):
        return 'Notiz in %s von %s' % (self.liste.bezeichnung, self.zeit_geaendert)
    
    class Meta: 
        ordering = ["-zeit_erstellt"]
        verbose_name = 'Notizzeile'
        verbose_name_plural = 'Notizzeilen'

