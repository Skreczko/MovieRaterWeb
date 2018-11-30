from django.conf.urls import url
from django.contrib import admin

from .views import ActorListAPIView, ActorDetailAPIView



urlpatterns = [
	url(r'^$', ActorListAPIView.as_view(), name='list'),
	url(r'^(?P<slug>[\w-]+)/$', ActorDetailAPIView.as_view(), name='detail'),

]
