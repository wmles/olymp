from django import template
from Grundgeruest.models import Nutzer

import ipdb

register = template.Library()

@register.simple_tag
def darf_teilnehmen(user, veranstaltung):
    """ ob der mich_eintragen-Link angezeigt werden soll, also im Prinzip
    ob der Nutzer schon in die Veranstaltung eingetragen ist; die ersten 
    zwei Fälle gesondert abfangen, da sonst Fehler bei db-Zugriff """
    if not user.is_authenticated():
        return False
    elif not hasattr(user.my_profile, 'person'):
        return True
    else:
        meine_veranstaltungen = [
            t.veranstaltung for t in 
            user.my_profile.person.teilnahme_set.all()]
        return veranstaltung not in meine_veranstaltungen
