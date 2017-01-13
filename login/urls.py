from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from login import views as core_views

urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^settings/$', core_views.settings, name='settings'),
    url(r'^settings/password/$', core_views.password, name='password'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
]

