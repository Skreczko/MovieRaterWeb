from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Movie, MovieComment, MovieGallery, MovieCategory
from .forms import MovieForm, MovieCategoryForm, MovieGalleryForm, MovieStarsForm
from datetime import datetime
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
# Create your views here.

"""------------------------MOVIE SECTION------------------------"""

							#MOVIE

class MovieListView(ListView):
	model = Movie
	#paginate_by = 2 dodaj strony z dokumentacji:
	""" 
	https://docs.djangoproject.com/en/2.1/topics/pagination/
	https://docs.djangoproject.com/en/2.1/topics/class-based-views/mixins/
	https://docs.djangoproject.com/en/2.1/ref/class-based-views/mixins/
	"""

	"""
	mozemy dodac wszystkie filmy danego reżysera na jednej stronie, zas innego na drugiej
	https://docs.djangoproject.com/en/2.1/topics/class-based-views/mixins/  <-Using SingleObjectMixin with ListView
	
	
	"""
	def get_queryset(self, *args, **kwargs):
		qs = super(MovieListView,self).get_queryset(*args, **kwargs).order_by("title")
		return qs


class MovieDetailView(FormMixin, DetailView):
	model = Movie
	form_class = MovieStarsForm



	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['gallery_movie_20'] = MovieGallery.objects.filter(movie=self.object)[:20]
		context['gallery_movie_all'] = MovieGallery.objects.filter(movie=self.object)
		context['user_vote'] = MovieComment.objects.filter(added_by=self.request.user, movie=self.object).first().stars
		return context

	def get_success_url(self):
		view_name = 'movie_detail'
		return reverse(view_name, kwargs={'slug': self.object.slug})

	def post(self, request, *args, **kwargs):
		# if not request.user.is_authenticated:
		# 	return HttpResponseForbidden()
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		stars = form.cleaned_data.get('stars')
		added_by = self.request.user
		check = MovieComment.objects.filter(added_by=added_by, movie=self.object)
		if check.exists():
			MovieComment.objects.filter(added_by=added_by, movie=self.object).update(stars=stars, edited_date=datetime.now())
		else:
			MovieComment.objects.create(stars=stars, movie=self.object, added_by=added_by).save()
		return super().form_valid(form)




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
		view_name = 'movie_detail'
		# No need for reverse_lazy here, because it's called inside the method
		return reverse(view_name, kwargs={'slug': self.object.slug})

class MovieDeleteView(DeleteView):
	model = Movie
	template_name = "confirm_delete.html"

	def get_success_url(self):
		return reverse("movie_list")



						#CATEGORY

def category_create(request, slug=None):
	qs_movie = Movie.objects.get(slug=slug)
	qs_category = MovieCategory.objects.filter(related_movie=qs_movie)
	form = MovieCategoryForm(request.POST or None, )
	template = 'form.html'
	context = {'form':form}


	if form.is_valid():
		category = form.cleaned_data['category']
		if len(qs_category) == 0:
			category = category[:]
		elif len(qs_category) == 1:
			category = category[:2]
		elif len(qs_category) == 2:
			category = category[:1]
		elif len(qs_category) == 3:
			category = []

		for item in category:
			check = MovieCategory.objects.filter(category=item).first()
			if not check:
				MovieCategory.objects.create(category=item).save()
			qs_category = MovieCategory.objects.filter(category=item).first()
			qs_category.related_movie.add(qs_movie)
		return redirect('movie_detail', slug)

	return render(request, template, context)

def category_edit(request, slug=None):
	qs_movie = Movie.objects.get(slug=slug)
	form = MovieCategoryForm(request.POST or None, )
	template = 'form.html'
	context = {'form':form}



	if form.is_valid():
		category = form.cleaned_data['category']
		if category:
			qs_movie.moviecategory_set.clear()
		for item in category:
			check = MovieCategory.objects.filter(category=item).first()
			if not check:
				MovieCategory.objects.create(category=item).save()
			qs_category = MovieCategory.objects.filter(category=item).first()
			qs_category.related_movie.add(qs_movie)
		return redirect('movie_detail', slug)

	return render(request, template, context)



							#GALLERY
def gallery_create(request, slug=None):
	qs_movie = Movie.objects.get(slug=slug)
	form = MovieGalleryForm(request.POST or None, request.FILES or None)
	template = 'form.html'
	context = {'form': form}

	if form.is_valid():
		picture = form.cleaned_data['picture']
		MovieGallery.objects.create(movie=qs_movie, picture=picture).save()
		return redirect('movie_detail', slug)

	return render(request, template, context)

class MovieGalleryView(DetailView):
	model = Movie
	template_name = 'movies/gallery.html'

def movie_gallery_delete(request, slug=None, id=None):
	photo = MovieGallery.objects.get(pk=id)
	print(photo.picture)
	template = "confirm_delete_gallery.html"
	context = {"photo": photo}
	if request.method == 'POST':
		photo.delete()
		return redirect('management_picture', slug)
	return render(request, template, context)



						# COMMENTS



