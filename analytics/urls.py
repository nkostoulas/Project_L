from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^analytics/$', views.analytics_main, name='analytics_main'),
	url(r'^analytics/(?P<selected_object>\d+)/(?P<selected_attribute>\w+)/$', views.analytics_selected, name='analytics_selected'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
