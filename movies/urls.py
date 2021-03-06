
from django.urls import path
from .views import MovieListView, MovieDetailView, MovieCreateView, MovieUpdateView, MovieDeleteView,\
					CommentsListView, CommentCreateView, CommentsUpdateView, CommentsDeleteView,\
					category_create, category_edit,\
					gallery_create, movie_gallery_delete,\
					cast_create, cast_edit, cast_delete, crew_create, crew_edit, crew_delete, \
					ErrorView

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
	path('detail/<slug>/gallery/', MovieDetailView.as_view(template_name = 'movies/gallery.html'), name='picture_gallery'),
	path('detail/<slug>/gallery/add_image/', gallery_create, name='add_picture'),
	path('detail/<slug>/gallery/management_image/', MovieDetailView.as_view(template_name = 'movies/gallery.html'),
		 name='management_picture'),
	path('detail/<slug>/gallery/delete/<id>', movie_gallery_delete, name='delete_picture'),

	#	MOVIES CAST
	path('detail/<slug>/cast/', MovieDetailView.as_view(template_name = 'movies/cast.html'), name='cast_list'),
	path('detail/<slug>/cast/add_role/', cast_create, name='add_cast'),
	path('detail/<slug>/cast/management_cast/editing/', MovieDetailView.as_view(template_name = 'movies/cast.html'),
		 																				name='management_cast_editing'),
	path('detail/<slug>/cast/management_cast/deleting/', MovieDetailView.as_view(template_name = 'movies/cast.html'),
		 																				name='management_cast_deleting'),
	path('detail/<slug>/cast/edit/<id>/', cast_edit, name='edit_cast'),
	path('detail/<slug>/cast/delete/<id>/', cast_delete, name='delete_cast'),

	#	MOVIES CREW
	path('detail/<slug>/crew/', MovieDetailView.as_view(template_name = 'movies/cast.html'), name='crew_list'),
	path('detail/<slug>/crew/add_role/', crew_create, name='add_crew'),
	path('detail/<slug>/crew/management_crew/editing/', MovieDetailView.as_view(template_name = 'movies/cast.html'),
		 																				name='management_crew_editing'),
	path('detail/<slug>/crew/management_crew/deleting/', MovieDetailView.as_view(template_name = 'movies/cast.html'),
		 																				name='management_crew_deleting'),
	path('detail/<slug>/crew/edit/<id>/', crew_edit, name='edit_crew'),
	path('detail/<slug>/crew/delete/<id>/', crew_delete, name='delete_crew'),


	#	MOVIE COMMENTS
	path('detail/<slug>/comments/', CommentsListView.as_view(), name='comment_list'),
	path('detail/<slug>/comments/add_comment/', CommentCreateView.as_view(), name='add_comment'),
	path('detail/comments/edit_comment/<int:pk>', CommentsUpdateView.as_view(), name='edit_comment'),
	path('detail/comments/delete_comment/<int:pk>', CommentsDeleteView.as_view(), name='delete_comment'),

	#	ERROR 404 TEMPLATE
	path('no-access/', ErrorView.as_view(), name='404-error'),



]