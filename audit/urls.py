"""audit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from task import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',  views.index, name='index'),
    url(r'^del/(\d+)$', views.delete_host, name='delete_host'),
    url(r'^play/(\d+)$',  views.play_host, name='play_host'),
    url(r'^host/(\d+)$',  views.host, name='host'),
    url(r'^score/(\d+)$', views.score, name='score'),
    url(r'^create_host$', views.create_host, name='create_host'),
    url(r'^add$', views.host_add, name='host_add'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
]
