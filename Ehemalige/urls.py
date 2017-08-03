from django.conf.urls import url, include
from django.views.generic import ListView
from . import views

app_name = 'Ehemalige'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^eintragen/$', views.EintragenView.as_view(), name='eintragen'),
]
