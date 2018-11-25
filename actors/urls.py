
from django.urls import path
from .views import ActorListView, ActorDetailView, ActorCreateView, \
					ActorUpdateView, ActorDeleteView, \
					ActorGalleryView, gallery_create, actor_gallery_delete

urlpatterns = [

	path('', ActorListView.as_view(), name='actor_list'),
	path('detail/<slug>/', ActorDetailView.as_view(), name='actor_detail'),
	path('detail/<slug>/edit/', ActorUpdateView.as_view(), name='actor_update'),
	path('detail/<slug>/delete/', ActorDeleteView.as_view(), name='actor_delete'),
	path('add/', ActorCreateView.as_view(), name='actor_create'),

	#	ACTOR GALLERY
	path('detail/<slug>/gallery/', ActorGalleryView.as_view(), name='actor_gallery'),
	path('detail/<slug>/gallery/add_image/', gallery_create, name='add_actor_picture'),
	path('detail/<slug>/gallery/management_image/', ActorGalleryView.as_view(), name='actor_management_picture'),
	path('detail/<slug>/gallery/delete/<id>', actor_gallery_delete, name='delete_actor_picture'),
]