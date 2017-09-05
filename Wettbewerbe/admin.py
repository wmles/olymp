from django.contrib import admin

import ipdb

from .models import *
from . import forms

admin.site.register(ArtTeilnahme)
admin.site.register(ArtVeranstaltung)
admin.site.register(WettbewerbsKategorie)
admin.site.register(Wettbewerb)
admin.site.register(Wettbewerbsjahrgang)


class TeilnahmeAdmin(admin.ModelAdmin):
    fields = [('person', 'nur_name'), 'veranstaltung', 'art']
    form = forms.TeilnahmeZuVeranstaltung
    search_fields = ['nur_name']

class TeilnahmeInline(admin.TabularInline):
    model = Teilnahme
    fields = ('person', 'nur_name', 'veranstaltung', 'art')
    extra = 1

admin.site.register(Teilnahme, TeilnahmeAdmin)

class KategorieInline(admin.TabularInline):
    model = WettbewerbsKategorie
    fields = ('bezeichnung', 'slug')
    extra = 1    

class ArtKategorieAdmin(admin.ModelAdmin):
    inlines = [KategorieInline]

class PersonAdmin(admin.ModelAdmin):
    inlines = [TeilnahmeInline]
    date_hierarchy = 'zeit_geaendert'
    anz_teilnahmen_ausgeben = lambda self, obj: obj.teilnahme_set.count()
    anz_teilnahmen_ausgeben.short_description = 'Anzahl der Teilnahmen'
    list_display = ['bezeichnung', 'nutzer', 'anz_teilnahmen_ausgeben']

class VeranstaltungAdmin(admin.ModelAdmin):
    inlines = [TeilnahmeInline]

admin.site.register(ArtKategorie, ArtKategorieAdmin)
admin.site.register(Veranstaltung, VeranstaltungAdmin)
admin.site.register(Person, PersonAdmin)
