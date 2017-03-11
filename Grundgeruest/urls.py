from django.conf.urls import url

from . import views

app_name = 'Grundgeruest'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
