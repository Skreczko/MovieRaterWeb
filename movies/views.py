from django.shortcuts import render
from django.urls import reverse
from .models import Movie, MovieComment, MovieGallery
from .forms import MovieForm

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.

class MovieListView(ListView):
	model = Movie

	def get_queryset(self, *args, **kwargs):
		qs = super(MovieListView,self).get_queryset(*args, **kwargs).order_by("title")
		return qs

class MovieDetailView(DetailView):
	model = Movie

class MovieCreateView(CreateView):

	template_name = "movies/movie_add.html"
	form_class = MovieForm

	def form_valid(self, form):
		return super(MovieCreateView,self).form_valid(form)

	def get_success_url(self):
		return reverse("movie_list")