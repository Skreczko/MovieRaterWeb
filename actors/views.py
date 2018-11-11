from django.shortcuts import render
from .models import Actor, ActorComment, ActorGallery

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


# Create your views here.

class ActorListView(ListView):
	model = Actor

	def get_queryset(self, *args, **kwargs):
		qs = super(ActorListView,self).get_queryset(*args, **kwargs).order_by("last_name")
		return qs

class ActorDetailView(DetailView):
	model = Actor