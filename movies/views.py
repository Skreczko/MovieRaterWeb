from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Movie

# Create your views here.

class MovieListView(ListView):
	model = Movie