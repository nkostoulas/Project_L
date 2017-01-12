from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.user_list, name='user_signup'),
    url(r'^signup/$', views.user_signup, name='user_signup'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
