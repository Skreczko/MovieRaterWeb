from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Actor, ActorComment, ActorGallery, ActorRole
from .forms import ActorForm, ActorGalleryForm, ActorStarsForm, \
					ActorCastForm, MovieCastRoleForm

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Create your views here.

class ActorListView(ListView):
	model = Actor
	paginate_by = 20
	queryset = Actor.objects.all()

	def get_queryset(self, *args, **kwargs):
		qs = super(ActorListView,self).get_queryset(*args, **kwargs).order_by("last_name")
		return qs

class ActorDetailView(FormMixin, DetailView):
	model = Actor
	form_class = ActorStarsForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['gallery_actor_20'] = ActorGallery.objects.filter(actor=self.object)[:20]
		context['gallery_actor_all'] = ActorGallery.objects.filter(actor=self.object)
		if ActorComment.objects.filter(added_by=self.request.user, actor=self.object).exists():
			context['user_vote'] = ActorComment.objects.filter(added_by=self.request.user, actor=self.object).first().stars
		return context

	def get_success_url(self):
		view_name = 'actor_detail'
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
		check = ActorComment.objects.filter(added_by=added_by, actor=self.object)
		if check.exists():
			ActorComment.objects.filter(added_by=added_by, actor=self.object).update(stars=stars)
		else:
			ActorComment.objects.create(stars=stars, actor=self.object, added_by=added_by).save()
		return super().form_valid(form)


class ActorCreateView(CreateView):
	template_name = "form.html"
	form_class = ActorForm

	def form_valid(self, form):
		return super(ActorCreateView,self).form_valid(form)

	def get_success_url(self):
		view_name = 'actor_detail'
		return reverse(view_name, kwargs={'slug': self.object.slug})

class ActorUpdateView(UpdateView):
	model = Actor
	template_name = "form.html"
	form_class = ActorForm


	def get_success_url(self):
		view_name = 'actor_detail'
		return reverse(view_name, kwargs={'slug': self.object.slug})

class ActorDeleteView(DeleteView):
	model=Actor
	template_name = "confirm_delete.html"

	def get_success_url(self):
		return reverse("actor_list")

					#GALLERY

def gallery_create(request, slug=None):
	qs_actor = Actor.objects.get(slug=slug)
	form = ActorGalleryForm(request.POST or None, request.FILES or None)
	template = 'form.html'
	context = {'form': form}

	if form.is_valid():
		picture = form.cleaned_data['picture']
		ActorGallery.objects.create(actor=qs_actor, picture=picture).save()
		return redirect('actor_detail', slug)

	return render(request, template, context)

class ActorGalleryView(DetailView):
	model = Actor
	template_name = 'actors/gallery.html'

def actor_gallery_delete(request, slug=None, id=None):
	photo = ActorGallery.objects.get(pk=id)
	template = "confirm_delete_gallery.html"
	context = {"photo": photo}
	if request.method == 'POST':
		photo.delete()
		return redirect('actor_management_picture', slug)
	return render(request, template, context)



							# CAST

class ActorCastView(DetailView):
	model = Actor
	template_name = 'actors/cast.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['related_movies'] = ActorRole.objects.filter(actor=self.object)
		return context

from django.forms.utils import ErrorList
from django import forms


def actor_cast_create(request, slug=None):
	qs_actor = Actor.objects.get(slug=slug)
	form = ActorCastForm(request.POST or None, request.FILES or None)
	template = 'form.html'
	context = {'form': form}
	if form.is_valid():
		movie = form.cleaned_data.get('movie')
		check = ActorRole.objects.filter(movie=movie, actor=qs_actor)
		if check.exists():
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
				u'Your cannot add more than one actor per movie!'
			])

		else:

			# ActorRole.objects.filter(movie=movie, actor=qs_actor).update(role=role, picture=picture)
		# else:
		# 	ActorRole.objects.create(movie=movie, actor=qs_actor, role=role, picture=picture).save()

			obj = form.save(commit=False)
			obj.actor = qs_actor
			print (obj.actor)

			obj.save()
			return redirect('actor_detail', slug)
	return render(request, template, context)


def actor_cast_edit(request, slug=None, id=None):
	qs_actor = Actor.objects.get(slug=slug)
	# qs_movie = Movie.objects.get(pk=id)
	qs_movie = Actor.actor_role.movie(pk=id)
	qs_cast = ActorRole.objects.get(movie=qs_movie, actor=qs_actor)
	form = MovieCastRoleForm(request.POST or None, request.FILES or None, instance=qs_cast)
	template = 'form.html'
	context = {'form': form}
	if form.is_valid():
		form.save()
		return redirect('actor_detail', slug)
	return render(request, template, context)

def actor_cast_delete(request, slug=None, id=None):
	qs_actor = Actor.objects.get(slug=slug)
	# qs_movie = Actor.objects.get(pk=id)
	qs_movie = Actor.actor_role.movie(pk=id)
	qs_cast = ActorRole.objects.get(movie=qs_movie, actor=qs_actor)
	template = "confirm_delete_gallery.html"
	context = {'role': qs_cast}
	if request.method == 'POST':
		qs_cast.delete()
		return redirect('movie_detail', slug)
	return render(request, template, context)

