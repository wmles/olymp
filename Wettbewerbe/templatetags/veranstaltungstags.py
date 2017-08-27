from django import template
from Wettbewerbe.models import Teilnahme

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

@register.simple_tag
def teilnahmen_sortiert(veranstaltung):
    """ gibt Liste der Teilnahmen in fancy Sortierung zurück 
    jetzt nach Art sortieren, später außerdem personen und strings trennen 
    und vll personen nach Geschlecht sortieren """
    return Teilnahme.objects.filter(veranstaltung=veranstaltung).order_by('art')
