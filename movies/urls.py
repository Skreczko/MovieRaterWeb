
from django.urls import path
from .views import MovieListView, MovieDetailView, MovieCreateView, MovieUpdateView, MovieDeleteView,\
					category_create

urlpatterns = [

	path('', MovieListView.as_view(), name='movie_list'),
	path('detail/<slug>', MovieDetailView.as_view(), name='movie_detail'),
	path('detail/<slug>/edit/', MovieUpdateView.as_view(), name='movie_update'),
	path('detail/<slug>/delete/', MovieDeleteView.as_view(), name='movie_delete'),
	path('add/', MovieCreateView.as_view(), name='movie_create'),

	path('cr/<id>', category_create, name='movie_category'),

]