# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from userena.models import UserenaSignup
from userena.settings import USERENA_ACTIVATED
from django.views.generic import ListView, DetailView, TemplateView
from django.db import transaction
import sqlite3 as lite
import pdb
from .models import *

def index(request):
    
    return render(
        request, 
        'base.html', 
        {})
    

