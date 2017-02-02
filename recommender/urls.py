from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^recommender/(?P<category>\d+)$', views.recommender, name='recommender'),	
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
