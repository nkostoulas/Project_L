from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^analytics/(?P<object>\d+)/(?P<user_attribute>\w+)/$', views.get_data_array, name='get_data_array'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
