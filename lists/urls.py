from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
	url(r'^logout/$', auth_views.logout, {'template_name': 'home.html'}, name='logout'),		
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^email/$', views.email, name='email'),
	url(r'^settings/$', views.settings, name='settings'),
	url(r'^submit_choice/$', views.submit_choice, name='submit_choice'),
	#url(r'^choose_category/$', views.choose_category, name='choose_category'),
	#url(r'^submit_lists/$', views.submit_lists, name='submit_lists'),
    url(r'^password/$', views.password, name='password'),
    url(r'^user_list/$', views.user_list, name='user_list'),	
    url(r'^$', views.home, name='home'),	
    url(r'^oauth/', include('social_django.urls', namespace='social')),
	url(r'^chaining', include('smart_selects.urls'))

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
