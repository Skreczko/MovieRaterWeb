
from django.urls import path
from .views import MovieListView, MovieDetailView, MovieCreateView, MovieUpdateView, MovieDeleteView,\
					MovieGalleryView, \
					MovieCastView,\
					category_create, category_edit,\
					gallery_create, movie_gallery_delete,\
					cast_create

urlpatterns = [
	#	MOVIES
	path('', MovieListView.as_view(), name='movie_list'),
	path('detail/<slug>', MovieDetailView.as_view(), name='movie_detail'),
	path('detail/<slug>/edit/', MovieUpdateView.as_view(), name='movie_update'),
	path('detail/<slug>/delete/', MovieDeleteView.as_view(), name='movie_delete'),
	path('add/', MovieCreateView.as_view(), name='movie_create'),



	#	MOVIES CATEGORIES
	path('detail/<slug>/add_category/', category_create, name='add_category'),
	path('detail/<slug>/edit_category/', category_edit, name='category_edit'),

	#	MOVIES GALLERY
	path('detail/<slug>/gallery/', MovieGalleryView.as_view(), name='picture_gallery'),
	path('detail/<slug>/gallery/add_image/', gallery_create, name='add_picture'),
	path('detail/<slug>/gallery/management_image/', MovieGalleryView.as_view(), name='management_picture'),
	path('detail/<slug>/gallery/delete/<id>', movie_gallery_delete, name='delete_picture'),
	#path('detail/<slug>/edit_category/', category_edit, name='category_edit'),

	#	MOVIES CAST
	path('detail/<slug>/cast/', MovieCastView.as_view(), name='cast_list'),
	path('detail/<slug>/gallery/add_role/', cast_create, name='add_cast'),
]