
from django.urls import path
from .views import ActorListView, ActorDetailView, ActorCreateView, \
					ActorUpdateView

urlpatterns = [

	path('', ActorListView.as_view(), name='actor_list'),
	path('detail/<slug>/', ActorDetailView.as_view(), name='actor_detail'),
	path('detail/<slug>/update/', ActorUpdateView.as_view(), name='actor_update'),
	path('add/', ActorCreateView.as_view(), name='actor_create'),


]