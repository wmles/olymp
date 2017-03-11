from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(ArtTeilnahme)
admin.site.register(ArtVeranstaltung)
admin.site.register(Veranstaltung)
admin.site.register(Person)
admin.site.register(Teilnahme)
admin.site.register(WettbewerbsKategorie)
admin.site.register(ArtKategorie)
admin.site.register(Unterseite)

