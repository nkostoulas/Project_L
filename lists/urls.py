from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.user_list, name='home')
]