from django.shortcuts import render, redirect, get_object_or_404
from django.forms.utils import ErrorList
from django import forms
from django.db.models import Q
from django.urls import reverse
from .models import Movie, MovieComment, MovieGallery, MovieCategory
from actors.models import Actor, ActorRole, CrewRole
from actors.forms import MovieCastForm, MovieCastRoleForm, \
							MovieCrewForm, MovieCrewRoleForm
from .forms import MovieForm, MovieCategoryForm, MovieGalleryForm, MovieStarsForm, MovieCommentForm
from datetime import datetime
from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
# Create your views here.

"""------------------------MOVIE SECTION------------------------"""

							#MOVIE

class MovieListView(ListView):
	model = Movie
	paginate_by = 20
	queryset = Movie.objects.all()
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
		context['related_actors'] = ActorRole.objects.filter(movie=self.object)
		context['related_crews'] = CrewRole.objects.filter(movie=self.object)
		context['director'] = CrewRole.objects.filter(movie=self.object, role='Director')
		context['comment_list'] = MovieComment.objects.filter(movie=self.object, added_by=self.request.user).exclude(Q(comment__isnull=True) | Q(comment__exact=''))[:5]
		if MovieComment.objects.filter(added_by=self.request.user, movie=self.object).exists():
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
			MovieComment.objects.filter(added_by=added_by, movie=self.object).update(stars=stars)
		else:
			MovieComment.objects.create(stars=stars, movie=self.object, added_by=added_by).save()
		return super().form_valid(form)




class MovieCreateView(CreateView):

	template_name = "form.html"
	form_class = MovieForm

	def form_valid(self, form):
		return super(MovieCreateView,self).form_valid(form)

	def get_success_url(self):
		view_name = 'movie_detail'
		return reverse(view_name, kwargs={'slug': self.object.slug})

class MovieUpdateView(UpdateView):
	model = Movie
	template_name = "form.html"
	form_class = MovieForm

	def get_success_url(self):
		view_name = 'movie_detail'
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
	template = "confirm_delete_gallery.html"
	context = {"photo": photo}
	if request.method == 'POST':
		photo.delete()
		return redirect('management_picture', slug)
	return render(request, template, context)



						# CAST

class MovieCastView(DetailView):
	model = Movie
	template_name = 'movies/cast.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['related_actors'] = ActorRole.objects.filter(movie=self.object)
		return context


def cast_create(request, slug=None):
	qs_movie = Movie.objects.get(slug=slug)
	form = MovieCastForm(request.POST or None, request.FILES or None)
	template = 'form.html'
	context = {'form': form}
	if form.is_valid():
		obj = form.save(commit=False)
		obj.movie = qs_movie
		obj.save()
		return redirect('movie_detail', slug)
	return render(request, template, context)


def cast_edit(request, slug=None, id=None):
	qs_movie = Movie.objects.get(slug=slug)
	qs_actor = Actor.objects.get(pk=id)
	qs_cast = ActorRole.objects.get(movie=qs_movie, actor=qs_actor)
	form = MovieCastRoleForm(request.POST or None, request.FILES or None, instance=qs_cast)
	template = 'form.html'
	context = {'form': form}
	if form.is_valid():
		form.save()
		return redirect('movie_detail', slug)
	return render(request, template, context)

def cast_delete(request, slug=None, id=None):
	qs_movie = Movie.objects.get(slug=slug)
	qs_actor = Actor.objects.get(pk=id)
	qs_cast = ActorRole.objects.get(movie=qs_movie, actor=qs_actor)
	template = "confirm_delete_gallery.html"
	context = {'role': qs_cast}
	if request.method == 'POST':
		qs_cast.delete()
		return redirect('movie_detail', slug)
	return render(request, template, context)



#							CREW
class MovieCrewView(DetailView):
	model = Movie
	template_name = 'movies/cast.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['related_crews'] = CrewRole.objects.filter(movie=self.object)
		return context



def crew_create(request, slug=None):
	qs_movie = Movie.objects.get(slug=slug)
	form = MovieCrewForm(request.POST or None, request.FILES or None)
	template = 'form.html'
	context = {'form': form}
	if form.is_valid():
		obj = form.save(commit=False)
		obj.movie = qs_movie
		obj.save()
		return redirect('movie_detail', slug)
	return render(request, template, context)


def crew_edit(request, slug=None, id=None):
	qs_movie = Movie.objects.get(slug=slug)
	qs_actor = Actor.objects.get(pk=id)
	qs_cast = CrewRole.objects.get(movie=qs_movie, actor=qs_actor)
	form = MovieCrewRoleForm(request.POST or None, request.FILES or None, instance=qs_cast)
	template = 'form.html'
	context = {'form': form}
	if form.is_valid():
		form.save()
		return redirect('movie_detail', slug)
	return render(request, template, context)

def crew_delete(request, slug=None, id=None):
	qs_movie = Movie.objects.get(slug=slug)
	qs_actor = Actor.objects.get(pk=id)
	qs_cast = CrewRole.objects.get(movie=qs_movie, actor=qs_actor)
	template = "confirm_delete_gallery.html"
	context = {'role': qs_cast}
	if request.method == 'POST':
		qs_cast.delete()
		return redirect('movie_detail', slug)
	return render(request, template, context)






#							COMMENTS

class CommentsListView(ListView):
	template_name = 'movies/comments.html'
	context_object_name = 'comment_list'
	paginate_by = 20

	def get_queryset(self):
		self.movie = get_object_or_404(Movie, slug=self.kwargs['slug'])
		return MovieComment.objects.filter(movie=self.movie).order_by('-publish_date','comment')



class CommentCreateView(CreateView):
	form_class = MovieCommentForm
	template_name = 'form_comment.html'

	def form_valid(self, form):
		movie = get_object_or_404(Movie, slug=self.kwargs.get('slug'))
		form.instance.movie = movie
		form.instance.added_by = self.request.user
		check = MovieComment.objects.filter(movie=movie, added_by=self.request.user)
		if check.exists():
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
				u'You have added comment already! Please check comment list.'
			])
			return super().form_invalid(form)
		else:
			return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['movie'] = get_object_or_404(Movie, slug=self.kwargs.get('slug'))
		return context

	def get_success_url(self):
		view_name = 'comment_list'
		return reverse(view_name, kwargs={'slug': self.object.movie.slug})



class CommentsUpdateView(UpdateView):
	model = MovieComment
	template_name = 'form_comment.html'
	form_class = MovieCommentForm

	def get_success_url(self):
		view_name = 'comment_list'
		return reverse(view_name, kwargs={'slug': self.object.movie.slug})


class CommentsDeleteView(DeleteView):
	model = MovieComment
	template_name = "confirm_delete.html"

	def get_success_url(self):
		return reverse("movie_list")



