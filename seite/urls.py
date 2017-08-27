"""seite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView#, ListView, DetailView, 

from Grundgeruest import userena_urls

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^olymp/', include('Wettbewerbe.urls')),
    url(r'^ehemalige/', include('Ehemalige.urls')),
    url(r'^todo/', include('Notizen.urls')),
    url(r'^nutzer/', include(userena_urls, namespace='')),

    url(r'^impressum/$', 
        TemplateView.as_view(
            template_name='impressum.html'), 
        name='impressum'),
    url(r'^$', 
        TemplateView.as_view(
            template_name='Grundgeruest/base.html'), 
        name='startseite'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
