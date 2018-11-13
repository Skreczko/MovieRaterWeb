from django.shortcuts import render
from django.urls import reverse
from .models import Actor, ActorComment, ActorGallery
from .forms import ActorForm

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Create your views here.

class ActorListView(ListView):
	model = Actor

	def get_queryset(self, *args, **kwargs):
		qs = super(ActorListView,self).get_queryset(*args, **kwargs).order_by("last_name")
		return qs

class ActorDetailView(DetailView):
	model = Actor

class ActorCreateView(CreateView):
	template_name = "form.html"
	form_class = ActorForm

	def form_valid(self, form):
		return super(ActorCreateView,self).form_valid(form)

	def get_success_url(self):
		return reverse("actor_list")

class ActorUpdateView(UpdateView):
	model = Actor
	template_name = "form.html"
	form_class = ActorForm
	prefix =

	def get_success_url(self):
		return reverse("actor_list")

class ActorDeleteView(DeleteView):
	model=Actor
	template_name = "confirm_delete.html"

	def get_success_url(self):
		return reverse("actor_list")


