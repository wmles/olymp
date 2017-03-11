"""
Die Modelle für Projektweite Daten: Nutzer/Profile

"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from django.core.validators import RegexValidator
import random, string


class Grundklasse(models.Model):
    bezeichnung = models.CharField(max_length=30)
    slug = models.SlugField(
        max_length=30, 
        null=False, 
        blank=True)
    zeit_erstellt = models.DateTimeField(
        auto_now_add=True,
        editable=False)
    zeit_geaendert = models.DateTimeField(
        auto_now=True,
        editable=False)
    
    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.bezeichnung)
        super(Grundklasse, self).save()

    def __str__(self):
        return str(self.bezeichnung)

    class Meta:
        abstract = True
        ordering = ["bezeichnung"]
        

class Nutzer(AbstractUser):
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = ''.join(random.sample(string.ascii_lowercase, 20))
        super(Nutzer, self).save(*args, **kwargs)

    class Meta: verbose_name_plural = 'Nutzer'
    

class Nutzerprofil(UserenaBaseProfile):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                unique=True,
                                verbose_name=_('Nutzer'),
                                related_name='my_profile')
    geschlecht = models.CharField(
        max_length=1,
        choices=[('weiblich', 'w'), ('männlich', 'm'), ('sonstiges', '')],
        default='m')
    tel = models.CharField(
        max_length=20,
        null=True, blank=True)
    strasse = models.CharField(
        max_length=30,
        blank=True)
    plz = models.CharField(
        max_length = 5,
        validators=[RegexValidator('^[0-9]+$')],
        blank=True)
    ort = models.CharField(
        max_length=30,
        blank=True)
    anredename = models.CharField(
        max_length=30,
        null=True, blank=True)

    class Meta():
        verbose_name = 'Nutzerprofil'
        verbose_name_plural = 'Nutzerprofile'
    

