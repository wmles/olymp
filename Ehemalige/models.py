from django.db import models

""" Konzept:

Man soll sich als Ehemaliger in die DB eintragen können (Nutzeraccount 
dafür nötig?)
Es gibt ein Textfeld für den Lebenslauf und die Auswahl des aktuellen Ortes 
und der Tätigkeit. 
ehem, das kommt mir ziemlich eng vor, so wie die alte Version der olymp-db

"""

from Grundgeruest.models import Grundklasse
from seite.settings import AUTH_USER_MODEL as user_model

class Ehemaliger(Grundklasse):
    """ Der Lebenslauf einer Person, optional Verknüpfung zum Nutzer """
    lebenslauf = models.TextField()
    ort = models.CharField(max_length=255)
    taetigkeit = models.CharField(max_length=255, verbose_name='Tätigkeit')
    nutzer = models.ForeignKey(user_model, null=True, blank=True)
    class Meta: 
        verbose_name_plural = 'Ehemalige'
