from django.contrib import admin
from django.forms import ModelForm

import ipdb

# Register your models here.

from .models import *

admin.site.register(ArtTeilnahme)
admin.site.register(ArtVeranstaltung)
admin.site.register(WettbewerbsKategorie)
admin.site.register(Unterseite)


class TeilnahmeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # das ist nicht schön, aber self.fields[...] lässt nur ein queryset
        # setzen und akzeptiert keine Liste, deshalb Umweg über pks
        liste_pks = [
            a.pk for a in ArtTeilnahme.objects.all()
            if self.instance.veranstaltung.art in a.artveranstaltung_set.all()
        ]
        self.fields['art'].queryset = ArtTeilnahme.objects.filter(pk__in=liste_pks)

class TeilnahmeAdmin(admin.ModelAdmin):
    fields = [('person', 'nur_name'), 'veranstaltung', 'art']
    form = TeilnahmeForm
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
