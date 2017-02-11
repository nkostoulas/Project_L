from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^recommender/(?P<category>\d+)/$', views.recommender, name='recommender'),
	url(r'^add_like/(?P<object>\d+)/$', views.add_like, name='add_like'),
	url(r'^add_dislike/(?P<object>\d+)/$', views.add_dislike, name='add_dislike'),
	url(r'^add_discard/(?P<object>\d+)/$', views.add_discard, name='add_discard'),
	url(r'^remove_from_like/(?P<object>\d+)/$', views.remove_from_like, name='remove_from_like'),
	url(r'^remove_from_dislike/(?P<object>\d+)/$', views.remove_from_dislike, name='remove_from_dislike'),
	url(r'^refresh_recommender/(?P<category>\d+)/$', views.refresh_recommender, name='refresh_recommender'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
