from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
	url(r'^callers/$', views.CallerList.as_view()),
	url(r'^callers/(?P<pk>[0-9]+)/$', views.CallerDetail.as_view()),
	url(r'^categories/$', views.CategoryList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)