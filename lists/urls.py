from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
	url(r'^logout/$', auth_views.logout, {'template_name': 'lists/user_list.html'}, name='logout'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^settings/$', views.settings, name='settings'),
    url(r'^password/$', views.password, name='password'),
	url(r'^oauth/', include('social_django.urls', namespace='social')),
	
    url(r'^$', views.user_list, name='user_list'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
