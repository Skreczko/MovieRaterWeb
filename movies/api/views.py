from django.db.models import Q
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
    )
from rest_framework import viewsets
from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination
from .serializers import  MovieListSerializer
from movies.models import Movie



class MovieListAPIView(ListAPIView):
	serializer_class = MovieListSerializer
	def get_queryset(self):
		queryset_list = Movie.objects.all()
		return queryset_list

