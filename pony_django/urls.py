"""pony_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from elder import views

urlpatterns = [
    url(r'^login', auth_views.login),
    url(r'^logout', auth_views.logout, {'next_page': 'registration/login.html'}),
    url(r'^password_change', auth_views.password_change),
    url(r'^password_change_done', auth_views.password_change_done),
    url(r'^password_reset', auth_views.password_reset),
    url(r'^password_reset_done', auth_views.password_reset_done),
    url(r'^password_reset_confirm', auth_views.password_reset_confirm),
    url(r'^password_reset_complete', auth_views.password_reset_complete),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^find/$', views.findoldperson, name='finoldperson'),
    url(r'^admin/', admin.site.urls),
]
