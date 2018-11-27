from django.shortcuts import render, redirect, get_object_or_404
from django.forms.utils import ErrorList
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from django.db.models import Q
from django.urls import reverse
from .models import Actor, ActorComment, ActorGallery, ActorRole, CrewRole
from .forms import ActorForm, ActorGalleryForm, ActorStarsForm, \
					ActorCastForm, MovieCastRoleForm, \
					ActorCrewForm, MovieCrewRoleForm,\
					ActorCommentForm

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import CREW_ROLE


# Create your views here.

class ActorListView(ListView):
	model = Actor
	paginate_by = 20
	queryset = Actor.objects.all()

	def get_queryset(self, *args, **kwargs):
		qs = super(ActorListView,self).get_queryset(*args, **kwargs).order_by('is_crew', 'last_name')
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
		context['related_movies'] = ActorRole.objects.filter(actor=self.object)
		context['related_crews'] = CrewRole.objects.filter(actor=self.object)
		context['comment_list'] = ActorComment.objects.filter(actor=self.object).exclude(
			Q(comment__isnull=True) | Q(comment__exact=''))[:5]
		context['all_comment_list'] = ActorComment.objects.filter(actor=self.object)
		context['your_comment_list'] = ActorComment.objects.filter(actor=self.object, added_by=self.request.user)
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

class ActorUpdateView(SuccessMessageMixin, UpdateView):
	model = Actor
	template_name = "form.html"
	form_class = ActorForm
	success_message = "%(name)s %(last_name)s was updated successfully!"


	def get_success_url(self):
		view_name = 'actor_detail'
		return reverse(view_name, kwargs={'slug': self.object.slug})

class ActorDeleteView(SuccessMessageMixin, DeleteView):
	model=Actor
	template_name = "confirm_delete.html"
	success_message = "Actor was deleted successfully!"

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super().delete(request, *args, **kwargs)

	def get_success_url(self):
		return reverse("actor_list")

					#GALLERY

def gallery_create(request, slug=None):
	qs_actor = Actor.objects.get(slug=slug)
	form = ActorGalleryForm(request.POST or None, request.FILES or None)
	template = 'form.html'
	context = {'form': form}

	if form.is_valid():
		messages.success(request, 'Image for {actor} has been added.'.format(actor=qs_actor))
		picture = form.cleaned_data['picture']
		ActorGallery.objects.create(actor=qs_actor, picture=picture).save()
		return redirect('actor_detail', slug)

	return render(request, template, context)

def actor_gallery_delete(request, slug=None, id=None):
	photo = ActorGallery.objects.get(pk=id)
	template = "confirm_delete_gallery.html"
	context = {"photo": photo}
	if request.method == 'POST':
		messages.success(request, 'Image  has been deleted.')
		photo.delete()
		return redirect('actor_management_picture', slug)
	return render(request, template, context)



							# CAST

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
			obj = form.save(commit=False)
			obj.actor = qs_actor
			obj.save()
			messages.success(request,
							 '{actor} playing in {title} has been added.'.format(actor=qs_actor, title=movie.title))
			return redirect('actor_detail', slug)
	return render(request, template, context)


def actor_cast_edit(request, slug=None, id=None):
	qs_cast = ActorRole.objects.get(pk=id)
	form = MovieCastRoleForm(request.POST or None, request.FILES or None, instance=qs_cast)
	template = 'form.html'
	context = {'form': form}
	if form.is_valid():
		form.save()
		messages.success(request,
						 '{actor} playing in {title} has been edited.'.format(actor=qs_cast.actor,
																			  title=qs_cast.movie.title))
		return redirect('actor_detail', slug)
	return render(request, template, context)

def actor_cast_delete(request, slug=None, id=None):
	qs_cast = ActorRole.objects.get(pk=id)
	template = "confirm_delete_gallery.html"
	context = {'role': qs_cast}
	if request.method == 'POST':
		qs_cast.delete()
		messages.success(request,
						 'Actor has been deleted.')
		return redirect('actor_detail', slug)
	return render(request, template, context)


#							CREW

def actor_crew_create(request, slug=None):
	qs_actor = Actor.objects.get(slug=slug)

	form = ActorCrewForm(request.POST or None, request.FILES or None)
	template = 'form.html'
	context = {'form': form}
	if form.is_valid():
		movie = form.cleaned_data.get('movie')
		check = CrewRole.objects.filter(movie=movie, actor=qs_actor)
		if check.exists():
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
				u'Your cannot add more than one actor per movie!'
			])
		else:
			obj = form.save(commit=False)
			obj.actor = qs_actor

			obj.save()
			messages.success(request,
							 '{actor} as a crew member of {title} has been added.'.format(actor=qs_actor, title=movie.title))
			return redirect('actor_detail', slug)
	return render(request, template, context)


def actor_crew_edit(request, slug=None, id=None):
	qs_cast = CrewRole.objects.get(pk=id)
	form = MovieCrewRoleForm(request.POST or None, request.FILES or None, instance=qs_cast)
	template = 'form.html'
	context = {'form': form}
	if form.is_valid():
		form.save()
		messages.success(request,
						 '{actor} as a crew member of {title} has been edited.'.format(actor=qs_cast.actor,
																					   title=qs_cast.movie.title))
		return redirect('actor_detail', slug)
	return render(request, template, context)

def actor_crew_delete(request, slug=None, id=None):
	qs_cast = CrewRole.objects.get(pk=id)
	template = "confirm_delete_gallery.html"
	context = {'role': qs_cast}
	if request.method == 'POST':
		qs_cast.delete()
		messages.success(request, 'Crew member has been deleted.')
		return redirect('actor_detail', slug)
	return render(request, template, context)



#							COMMENTS

class CommentsListView(ListView):
	template_name = 'comments.html'
	context_object_name = 'comment_list'
	paginate_by = 10

	def get_queryset(self):
		self.actor = get_object_or_404(Actor, slug=self.kwargs['slug'])
		return ActorComment.objects.filter(actor=self.actor).order_by('-publish_date', 'comment')



class CommentCreateView(SuccessMessageMixin, CreateView):
	form_class = ActorCommentForm
	template_name = 'form_comment.html'
	success_message = "Your comment was created successfully!"

	def form_valid(self, form):
		actor = get_object_or_404(Actor, slug=self.kwargs.get('slug'))
		form.instance.actor = actor
		form.instance.added_by = self.request.user
		check = ActorComment.objects.filter(actor=actor, added_by=self.request.user)
		if check.exists():
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
				u'You have added comment already! Please check comment list.'
			])
			return super().form_invalid(form)
		else:
			return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['actor'] = get_object_or_404(Actor, slug=self.kwargs.get('slug'))
		return context

	def get_success_url(self):
		view_name = 'actor_comment_list'
		return reverse(view_name, kwargs={'slug': self.object.actor.slug})



class CommentsUpdateView(SuccessMessageMixin, UpdateView):
	model = ActorComment
	template_name = 'form_comment.html'
	form_class = ActorCommentForm
	success_message = "Your comment was updated successfully!"

	def get_success_url(self):
		view_name = 'actor_comment_list'
		return reverse(view_name, kwargs={'slug': self.object.actor.slug})


class CommentsDeleteView(SuccessMessageMixin, DeleteView):
	model = ActorComment
	template_name = "confirm_delete.html"
	success_message = "Your comment was deleted successfully!"

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super().delete(request, *args, **kwargs)

	def get_success_url(self):
		return reverse("actor_list")