from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

	#	lists views
	url(r'^$', views.home, name='home'),	
    #url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
	url(r'^logout/$', auth_views.logout, {'template_name': 'projectl/home.html'}, name='logout'),		
	url(r'^email/$', views.email, name='email'),
	url(r'^user_list/$', views.user_list, name='user_list'),	
	url(r'^edit/(?P<category>\d+)/$', views.edit, name='edit'),

	#	from apps
    url(r'^oauth/', include('social_django.urls', namespace='social')),

	#	MIGHT USE IN THE FUTURE
	#url(r'^password/$', views.password, name='password'),
	#url(r'^signup/$', views.signup, name='signup'),
	#url(r'^settings/$', views.settings, name='settings')
	
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
