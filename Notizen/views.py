from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from . import models
import ipdb

# Create your views here.

class ZeigenUndEintragen(CreateView):
    """ zeigt die bisher einzige Liste an """
    template_name = 'Notizen/liste.html'
    model = models.Zeile
    fields = ['autor_name', 'text']
    context_object_name = 'liste'
    
    def get_success_url(self, *args, **kwargs):
        return reverse('Notizen:liste')

    def render_to_response(self, context, **kwargs):
        """ Gibt eine Instanz von TemplateResponse zurück
        ich übergebe der zusätzlich eine Liste aller Zeilen; später nur die 
        zugehörigen zu einer models.Liste """
        response = super().render_to_response(context, **kwargs)
        # übergebe Liste von Zeilen
        response.context_data.update([
            ('liste', models.Zeile.objects.all())
        ])
        return response
        
    def form_valid(self, form):
        """ Setzt autor und liste für die Notizzeile.
        form.instance wurde vor dem Aufrufen davon erstellt, nur noch nicht
        in die db geschrieben (wär ja auch nicht valide); vorher müssen die 
        null=False-Felder gesetzt werden """
        form.instance.autor_id = self.request.user.pk
        form.instance.liste_id = int(self.kwargs['liste_id'])
        form.instance.save()
        return super().form_valid(form)
