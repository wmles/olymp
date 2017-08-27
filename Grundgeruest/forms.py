from django.contrib.auth import get_user_model
from hashlib import sha1
import random
from userena.forms import SignupForm

def erzeuge_zufall(laenge, sonderzeichen=3):
    """ gibt Zufallsstring zurück, wobei die Zeichen abwechselnd aus den 
    Listen in s gewählt werden; sonderzeichen<4 wählt nicht alle Listen """
    s = ['abcdefghijkmnopqrstuvwxyz',
        'ABCDEFGHJKLMNPQRSTUVWXYZ',
        '23456789_-', 
        '@.%&+!$?/()#*']
    zufall = []
    for i in range(laenge):
        zufall.append(random.sample(s[i % sonderzeichen], 1)[0])
    return ''.join(zufall)    

class FormularRegistrierung(SignupForm):
    """
    Kopiert und angepasst aus SigninFormOnlyEmail aus userena.forms
    
    Habe autogenerierten Namen geändert.
    """
    def __init__(self, *args, **kwargs):
        super(FormularRegistrierung, self).__init__(*args, **kwargs)
        del self.fields['username']

    def save(self):
        """ Generate a random username before falling back to parent signup form """
        while True:
            username = erzeuge_zufall(7)
            try:
                get_user_model().objects.get(username__iexact=username)
            except get_user_model().DoesNotExist: break

        self.cleaned_data['username'] = username
        return super(FormularRegistrierung, self).save()

