
from django.urls import path
from .views import ActorListView, ActorDetailView, ActorCreateView, \
					ActorUpdateView, ActorDeleteView

urlpatterns = [

	path('', ActorListView.as_view(), name='actor_list'),
	path('detail/<slug>/', ActorDetailView.as_view(), name='actor_detail'),
	path('detail/<slug>/edit/', ActorUpdateView.as_view(), name='actor_update'),
	path('detail/<slug>/delete/', ActorDeleteView.as_view(), name='actor_delete'),
	path('add/', ActorCreateView.as_view(), name='actor_create'),
]