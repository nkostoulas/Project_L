from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^recommender/(?P<category>\d+)/$', views.recommender, name='recommender'),
	url(r'^add_like/(?P<object>\d+)/$', views.add_like, name='add_like'),
	url(r'^add_dislike/(?P<object>\d+)/$', views.add_dislike, name='add_dislike'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
