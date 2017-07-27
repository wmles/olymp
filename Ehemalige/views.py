from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class IndexView(TemplateView):
    """ zeigt die Startseite an :) """
    template_name = 'Ehemalige/index.html'
