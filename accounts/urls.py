from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register),
    path('register/<activation_key>', views.activate_user),


]