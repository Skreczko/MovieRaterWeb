from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Movie, MovieComment, MovieGallery, MovieCategory
from .forms import MovieForm, MovieCategoryForm

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
# Create your views here.

"""------------------------MOVIE SECTION------------------------"""

							#MOVIE

class MovieListView(ListView):
	model = Movie

	def get_queryset(self, *args, **kwargs):
		qs = super(MovieListView,self).get_queryset(*args, **kwargs).order_by("title")
		return qs


class MovieDetailView(DetailView):
	model = Movie

class MovieCreateView(CreateView):

	template_name = "form.html"
	form_class = MovieForm

	def form_valid(self, form):
		return super(MovieCreateView,self).form_valid(form)

	def get_success_url(self):
		return reverse("movie_list")

class MovieUpdateView(UpdateView):
	model = Movie
	template_name = "form.html"
	form_class = MovieForm

	def get_success_url(self):
		return reverse("movie_list")

class MovieDeleteView(DeleteView):
	model = Movie
	template_name = "confirm_delete.html"

	def get_success_url(self):
		return reverse("movie_list")


						#CATEGORY

def category_create(request, slug=None):
	form = MovieCategoryForm(request.POST or None)
	qs_movie = Movie.objects.get(slug=slug)

	if form.is_valid():
		category = form.cleaned_data['category']
		for item in category:
			check = MovieCategory.objects.filter(category=item).first()
			if not check:
				MovieCategory.objects.create(category=item).save()
			qs_category = MovieCategory.objects.filter(category=item).first()
			qs_category.related_movie.add(qs_movie)
		return redirect('movie_detail', slug)

	return render(request, 'form.html', {'form':form})

# def category_edit(request, slug=None):
# 	form = MovieCategoryForm(request.POST or None)
# 	qs_movie = Movie.objects.get(slug=slug)
#
# 	if form.is_valid():
# 		category = form.cleaned_data['category']
# 		for item in category:
# 			check = MovieCategory.objects.filter(category=item).first()
# 			if not check:
# 				MovieCategory.objects.create(category=item).save()
# 			qs_category = MovieCategory.objects.filter(category=item).first()
# 			qs_category.related_movie.add(qs_movie)
# 		return redirect('movie_detail', slug)
#
# 	return render(request, 'form.html', {'form': form}

		#GALLERY
