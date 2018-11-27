
from django.urls import path
from .views import ActorListView, ActorDetailView, ActorCreateView, \
					ActorUpdateView, ActorDeleteView, \
					gallery_create, actor_gallery_delete,\
					 actor_cast_create, actor_cast_edit, actor_cast_delete

urlpatterns = [

	path('', ActorListView.as_view(), name='actor_list'),
	path('detail/<slug>/', ActorDetailView.as_view(), name='actor_detail'),
	path('detail/<slug>/edit/', ActorUpdateView.as_view(), name='actor_update'),
	path('detail/<slug>/delete/', ActorDeleteView.as_view(), name='actor_delete'),
	path('add/', ActorCreateView.as_view(), name='actor_create'),

	#	ACTOR GALLERY
	path('detail/<slug>/gallery/', ActorDetailView.as_view(template_name = 'actors/gallery.html'), name='actor_gallery'),
	path('detail/<slug>/gallery/add_image/', gallery_create, name='add_actor_picture'),
	path('detail/<slug>/gallery/management_image/', ActorDetailView.as_view(template_name = 'actors/gallery.html'), name='actor_management_picture'),
	path('detail/<slug>/gallery/delete/<id>', actor_gallery_delete, name='delete_actor_picture'),

	#	ACTING IN MOVIE
	path('detail/<slug>/cast/', ActorDetailView.as_view(template_name = 'actors/cast.html'), name='actor_cast_list'),
	path('detail/<slug>/cast/add_role/', actor_cast_create, name='actor_add_cast'),
	path('detail/<slug>/cast/management_cast/editing/', ActorDetailView.as_view(template_name = 'actors/cast.html'), name='actor_management_cast_editing'),
	path('detail/<slug>/cast/management_cast/deleting/', ActorDetailView.as_view(template_name = 'actors/cast.html'), name='actor_management_cast_deleting'),
	path('detail/<slug>/cast/edit/<id>/', actor_cast_edit, name='actor_edit_cast'),
	path('detail/<slug>/cast/delete/<id>/', actor_cast_delete, name='actor_delete_cast'),
]