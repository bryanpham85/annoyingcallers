from django.conf.urls import url
from api import views

urlpatterns = [
	url(r'^callers/$', views.caller_list),
	url(r'^callers/(?P<pk>[0-9]+)/$', views.caller_detail),
]