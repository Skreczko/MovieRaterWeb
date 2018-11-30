from django.conf.urls import url
from django.contrib import admin

from .views import MovieListAPIView



urlpatterns = [
	url(r'^$', MovieListAPIView.as_view(), name='list'),
	url(r'^$', MovieListAPIView.as_view(), name='list'),

]
