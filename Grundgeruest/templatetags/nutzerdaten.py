from django import template
from Grundgeruest.models import Nutzer

register = template.Library()

@register.inclusion_tag('Grundgeruest/kopfzeile_knopf.html')
def kopfleiste_knoepfe(user):
    """ Der tag erwartet von der Funktion ein dict, in dem die Liste der 
    url-text-Paare für die Knöpfe der Kopfleiste steht """
    
    return {'knoepfe': Nutzer.knoepfe_kopf(user)}

@register.inclusion_tag('Grundgeruest/menueleiste_knopf.html')
def menueleiste_knoepfe(user):
    """ gibt ein dict zurück, in dem die Liste der url-text-Paare für die
    Knöpfe der Menüleiste steht """
    
    return {'knoepfe': Nutzer.knoepfe_menü(user)}
