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
from django.template.defaultfilters import slugify
from django.urls import reverse


class MinimalModel(models.Model):
    zeit_erstellt = models.DateTimeField(
        auto_now_add=True,
        editable=False)
    zeit_geaendert = models.DateTimeField(
        auto_now=True,
        editable=False)

    class Meta:
        abstract = True
        ordering = ["-zeit_geaendert"]

    def __str__(self):
        return self.__class__().__name__() + ' geändert ' + str(zeit_geaendert)

class Grundklasse(MinimalModel):
    bezeichnung = models.CharField(max_length=30)
    slug = models.SlugField(
        max_length=30, 
        null=False, 
        blank=True)
    
    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.bezeichnung)
        super(Grundklasse, self).save()

    class Meta:
        abstract = True
        ordering = ["bezeichnung"]
        
    def __str__(self):
        return str(self.bezeichnung)


def knoepfe_kopf(user):
    """ gibt Knöpfe für Kopfleiste als Liste von Tupeln zurück """
    anmelden = (reverse('userena_signin'), 'Anmelden')
    registrieren = (reverse('userena_signup'), 'Registrieren') 
    abmelden = (reverse('userena_signout'), 'Abmelden')
    profil = lambda nutzer: (reverse('userena_profile_detail', 
                    kwargs={'username': nutzer.username}), 'Profil') 
    spam = ('spam', 'spam') 
    
    if user.username == 'admin':
        return [abmelden, profil(user), spam]        
    elif user.is_authenticated():
        return [abmelden, profil(user)]
    else:
        return [anmelden, registrieren]

def knoepfe_menü(user):
    """ gibt Knöpfe für Menüleiste als Liste von Tupeln zurück """
    alle = {
        'index': ('/', 'Startseite'), 
        'olymp': (reverse('Wettbewerbe:index'), 'Wettbewerbe'), 
        'ehemalige': (reverse('Ehemalige:index'), 'Ehemalige'),
        'spam': ('spam', 'spam'), 
        'impressum': (reverse('impressum'), 'Impressum'),
        'db': ('https://olymp.piokg.de/static/db.pdf', 'Datenbanklayout'), # quick and very dirty :)
    }
    
    if user.username == 'admin':
        return [alle[name] for name in ('index', 'olymp', 'ehemalige', 'spam', 'db')]
    else:
        return [alle[name] for name in ('index', 'olymp', 'impressum')]
        

class Nutzer(AbstractUser):
    """ Nutzer-Klasse """
    def knoepfe_kopf(nutzer):
        """ soll Liste von Paaren für Knöpfe der Kopfleiste ausgeben 
        Nutzt im Moment die module-fkt gleichen Namens, könnte später vll
        die Gruppenzugehörigkeit heranziehen, etc, ist flexibel """
        return knoepfe_kopf(nutzer)

    def knoepfe_menü(self):
        """ soll Liste von Paaren für Knöpfe der Menüleiste ausgeben 
        Nutzt im Moment die module-fkt gleichen Namens, könnte später vll
        die Gruppenzugehörigkeit heranziehen, etc, ist flexibel """
        return knoepfe_menü(self)
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = ''.join(random.sample(string.ascii_lowercase, 20))
        super(Nutzer, self).save(*args, **kwargs)

    class Meta: 
        verbose_name_plural = 'Nutzer'
        verbose_name = 'Nutzer'
    
    def __str__(self):
        return 'Nutzer %s %s (%s)' % (self.first_name, self.last_name, self.email)
    

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
    
