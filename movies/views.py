from django.shortcuts import render, redirect, get_object_or_404
from django.forms.utils import ErrorList
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse
from .models import Movie, MovieComment, MovieGallery, MovieCategory
from django import forms
from actors.models import Actor, ActorRole, CrewRole
from actors.forms import MovieCastForm, MovieCastRoleForm, \
							MovieCrewForm, MovieCrewRoleForm
from .forms import MovieForm, MovieCategoryForm, MovieGalleryForm, MovieStarsForm, MovieCommentForm
from actors.models import CREW_ROLE

from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


# Create your views here.

"""------------------------PERMISSIONS------------------------"""
class ErrorView(TemplateView):
	template_name = "404.html"

class IsStaffMixin(UserPassesTestMixin):
	def test_func(self):
		return self.request.user.is_staff


def is_staff_check(user):
	return user.is_staff

"""------------------------MOVIE SECTION------------------------"""

							#MOVIE

class MovieListView(ListView):
	model = Movie
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['director'] = CrewRole.objects.all()
		context['check_director'] = str('Director')
		context['actors_in_movie'] = ActorRole.objects.all()
		return context

	def get_queryset(self, *args, **kwargs):
		qs = super().get_queryset(*args, **kwargs).order_by("title")
		query = self.request.GET.get('q', None)
		if query is not None:
			qs = qs.filter(
				Q(title__icontains=query)
			)
		return qs


class MovieDetailView(FormMixin, DetailView):
	model = Movie
	form_class = MovieStarsForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['gallery_movie_20'] = MovieGallery.objects.filter(movie=self.object)[:20]
		context['gallery_movie_all'] = MovieGallery.objects.filter(movie=self.object)
		context['related_actors'] = ActorRole.objects.filter(movie=self.object).order_by('-movie')
		context['related_crews'] = CrewRole.objects.filter(movie=self.object).order_by('-movie')
		context['director'] = CrewRole.objects.filter(movie=self.object, role='Director')
		context['comment_list'] = MovieComment.objects.filter(movie=self.object).exclude(Q(comment__isnull=True) | Q(comment__exact=''))[:5]
		context['all_comment_list'] = MovieComment.objects.filter(movie=self.object)
		context['related_category'] = MovieCategory.objects.filter(related_movie=self.object)
		if self.request.user.is_authenticated:
			context['your_comment_list'] = MovieComment.objects.filter(movie=self.object, added_by=self.request.user)
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



class MovieCreateView(LoginRequiredMixin, IsStaffMixin, CreateView):

	template_name = "form.html"
	form_class = MovieForm
	login_url = "404-error"
	def form_valid(self, form):
		return super(MovieCreateView,self).form_valid(form)

	def get_success_url(self):
		view_name = 'movie_detail'
		return reverse(view_name, kwargs={'slug': self.object.slug})



class MovieUpdateView(LoginRequiredMixin, IsStaffMixin, SuccessMessageMixin, UpdateView):
	model = Movie
	template_name = "form.html"
	form_class = MovieForm
	success_message = "%(title)s was updated successfully!"
	login_url = "404-error"

	def get_success_url(self):
		view_name = 'movie_detail'
		return reverse(view_name, kwargs={'slug': self.object.slug})



class MovieDeleteView(LoginRequiredMixin, IsStaffMixin, SuccessMessageMixin, DeleteView):
	model = Movie
	template_name = "confirm_delete.html"
	success_message = "Movie was deleted successfully!"
	login_url = "404-error"

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super().delete(request, *args, **kwargs)

	def get_success_url(self):
		return reverse("movie_list")



						#CATEGORY

@user_passes_test(is_staff_check, login_url='404-error')
def category_create(request, slug=None):
	qs_movie = Movie.objects.get(slug=slug)
	qs_category = MovieCategory.objects.filter(related_movie=qs_movie)
	form = MovieCategoryForm(request.POST or None, )
	template = 'form.html'
	context = {'form':form}
	if form.is_valid():
		messages.success(request, 'Category for {title} has been added.'.format(title=qs_movie.title))
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



@user_passes_test(is_staff_check, login_url='404-error')
def category_edit(request, slug=None):
	qs_movie = Movie.objects.get(slug=slug)
	form = MovieCategoryForm(request.POST or None, )

	template = 'form.html'
	context = {'form':form}

	if form.is_valid():
		category = form.cleaned_data['category']
		if category:
			qs_movie.movie_category.clear()
		for item in category:
			check = MovieCategory.objects.filter(category=item).first()
			if not check:
				MovieCategory.objects.create(category=item).save()
			qs_category = MovieCategory.objects.filter(category=item).first()
			qs_category.related_movie.add(qs_movie)
		messages.success(request, 'Category for {title} has been changed.'.format(title=qs_movie.title))
		return redirect('movie_detail', slug)

	return render(request, template, context)



							#GALLERY

@login_required(login_url='404-error')
@user_passes_test(is_staff_check, login_url='404-error')
def gallery_create(request, slug=None):
	qs_movie = Movie.objects.get(slug=slug)
	form = MovieGalleryForm(request.POST or None, request.FILES or None)
	template = 'form.html'
	context = {'form': form}

	if form.is_valid():
		messages.success(request, 'Image for {title} has been added.'.format(title=qs_movie.title))
		picture = form.cleaned_data['picture']
		MovieGallery.objects.create(movie=qs_movie, picture=picture).save()
		return redirect('movie_detail', slug)

	return render(request, template, context)


@login_required(login_url='404-error')
@user_passes_test(is_staff_check, login_url='404-error')
def movie_gallery_delete(request, slug=None, id=None):
	photo = MovieGallery.objects.get(pk=id)
	template = "confirm_delete_gallery.html"
	context = {"photo": photo}
	if request.method == 'POST':
		photo.delete()
		messages.success(request, 'Image  has been deleted.')
		return redirect('management_picture', slug)
	return render(request, template, context)



						# CAST

@login_required(login_url='404-error')
@user_passes_test(is_staff_check, login_url='404-error')
def cast_create(request, slug=None):
	qs_movie = Movie.objects.get(slug=slug)
	form = MovieCastForm(request.POST or None, request.FILES or None)
	template = 'form.html'
	context = {'form': form}
	if form.is_valid():
		actor = form.cleaned_data.get('actor')
		check = ActorRole.objects.filter(actor=actor, movie=qs_movie)
		if check.exists() and check.first().role not in CREW_ROLE:
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
				u'Your cannot add more than one actor per movie!'
			])
		else:
			obj = form.save(commit=False)
			obj.movie = qs_movie
			obj.save()
			messages.success(request, '{actor} playing in {title} has been added.'.format(actor=actor, title=qs_movie.title))
			return redirect('movie_detail', slug)
	return render(request, template, context)



@login_required(login_url='404-error')
@user_passes_test(is_staff_check, login_url='404-error')
def cast_edit(request, slug=None, id=None):
	qs_cast = ActorRole.objects.get(pk=id)
	form = MovieCastRoleForm(request.POST or None, request.FILES or None, instance=qs_cast)
	template = 'form.html'
	context = {'form': form}
	if form.is_valid():
		form.save()
		messages.success(request,
						 '{actor} playing in {title} has been edited.'.format(actor=qs_cast.actor, title=qs_cast.movie.title))
		return redirect('movie_detail', slug)
	return render(request, template, context)



@login_required(login_url='404-error')
@user_passes_test(is_staff_check, login_url='404-error')
def cast_delete(request, slug=None, id=None):
	qs_cast = ActorRole.objects.get(pk=id)
	template = "confirm_delete_gallery.html"
	context = {'role': qs_cast}
	if request.method == 'POST':
		qs_cast.delete()
		messages.success(request,
						 'Actor has been deleted.')
		return redirect('movie_detail', slug)
	return render(request, template, context)



#							CREW

@login_required(login_url='404-error')
@user_passes_test(is_staff_check, login_url='404-error')
def crew_create(request, slug=None):
	qs_movie = Movie.objects.get(slug=slug)
	form = MovieCrewForm(request.POST or None, request.FILES or None)
	template = 'form.html'
	context = {'form': form}
	if form.is_valid():
		actor = form.cleaned_data.get('actor')
		check = CrewRole.objects.filter(actor=actor, movie=qs_movie)
		if check.exists():
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
				u'Your cannot add more than one actor per movie!'
			])
		else:
			obj = form.save(commit=False)
			obj.movie = qs_movie
			obj.save()
			messages.success(request,
							 '{actor} as a crew member of {title} has been added.'.format(actor=actor, title=qs_movie.title))
			return redirect('movie_detail', slug)
	return render(request, template, context)



@login_required(login_url='404-error')
@user_passes_test(is_staff_check, login_url='404-error')
def crew_edit(request, slug=None, id=None):
	qs_cast = CrewRole.objects.get(pk=id)
	form = MovieCrewRoleForm(request.POST or None, request.FILES or None, instance=qs_cast)
	template = 'form.html'
	context = {'form': form}
	if form.is_valid():
		form.save()
		messages.success(request,
						 '{actor} as a crew member of {title} has been edited.'.format(actor=qs_cast.actor,
																					  title=qs_cast.movie.title))
		return redirect('movie_detail', slug)
	return render(request, template, context)



@login_required(login_url='404-error')
@user_passes_test(is_staff_check, login_url='404-error')
def crew_delete(request, slug=None, id=None):
	qs_cast = CrewRole.objects.get(pk=id)
	template = "confirm_delete_gallery.html"
	context = {'role': qs_cast}
	if request.method == 'POST':
		qs_cast.delete()
		messages.success(request, 'Crew member has been deleted.')
		return redirect('movie_detail', slug)
	return render(request, template, context)




#							COMMENTS

class CommentsListView(ListView):
	template_name = 'comments.html'
	context_object_name = 'comment_list'
	paginate_by = 10
	login_url = "404-error"
	def get_queryset(self):
		self.movie = get_object_or_404(Movie, slug=self.kwargs['slug'])
		return MovieComment.objects.filter(movie=self.movie).order_by('-publish_date', 'comment')



class CommentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	form_class = MovieCommentForm
	template_name = 'form_comment.html'
	success_message = "Your comment was created successfully!"
	login_url = "404-error"

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


class CommentsUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	model = MovieComment
	template_name = 'form_comment.html'
	form_class = MovieCommentForm
	success_message = "Your comment was updated successfully!"
	login_url = "404-error"

	def get_success_url(self):
		view_name = 'comment_list'
		return reverse(view_name, kwargs={'slug': self.object.movie.slug})



class CommentsDeleteView(LoginRequiredMixin,  SuccessMessageMixin, DeleteView):
	model = MovieComment
	template_name = "confirm_delete.html"
	success_message = "Your comment was deleted successfully!"
	login_url = "404-error"

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super().delete(request, *args, **kwargs)

	def get_success_url(self):
		return reverse("movie_list")



