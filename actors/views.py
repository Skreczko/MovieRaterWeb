from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Actor, ActorComment, ActorGallery
from .forms import ActorForm, ActorGalleryForm

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Create your views here.

class ActorListView(ListView):
	model = Actor
	paginate_by = 20
	queryset = Actor.objects.all()

	def get_queryset(self, *args, **kwargs):
		qs = super(ActorListView,self).get_queryset(*args, **kwargs).order_by("last_name")
		return qs

class ActorDetailView(DetailView):
	model = Actor

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['gallery_actor_20'] = ActorGallery.objects.filter(actor=self.object)[:20]
		context['gallery_actor_all'] = ActorGallery.objects.filter(actor=self.object)
		return context


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
