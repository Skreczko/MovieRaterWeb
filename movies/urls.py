
from django.urls import path
from .views import MovieListView, MovieDetailView, MovieCreateView

urlpatterns = [

	path('', MovieListView.as_view(), name='movie_list'),
	path('detail/<slug>', MovieDetailView.as_view(), name='movie_detail'),
	path('add/', MovieCreateView.as_view(), name='movie_create'),

]