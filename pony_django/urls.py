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
    url(r'^login/$', views.login, name='login'), #localhost:8000/login/
    url(r'^logout', views.logout, name='logout'),
    url(r'^password_reset/$', views.password_reset, name='password_reset'),
    url(r'^password_reset_done$', views.password_reset, name='password_reset_done'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^matching/$', views.matching, name='matching'),
    url(r'^suggest/$', views.suggest, name='suggest'),
    url(r'^proposal/$', views.proposal, name='proposal'),
    url(r'^find/$', views.findoldperson, name='findoldperson'),
    url(r'^other/$', views.otherprofile, name='other'),
    url(r'^update/$', views.update, name='update'),
    url(r'^usercontact/$', views.user_contact, name='usercontact'),
    url(r'^admin/', admin.site.urls),
]
