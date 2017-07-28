from django.contrib import admin

import ipdb

# Register your models here.

from .models import *

admin.site.register(Liste)
admin.site.register(Zeile)

