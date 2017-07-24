from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
	url(r'^api/callers/$', views.CallerList.as_view()),
	url(r'^api/callers/(?P<pk>[0-9]+)/$', views.CallerDetail.as_view()),
	url(r'^api/categories/$', views.CategoryList.as_view()),
	url(r'^api/device/$', views.DeviceList.as_view()),
	url(r'^api/device/(?P<deviceId>[a-z0-9]+)/$', views.DeviceDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)