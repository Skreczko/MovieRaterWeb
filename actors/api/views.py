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
from movies.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination

from .serializers import ActorListSerializer, ActorDetailSerializer
from actors.models import Actor



class ActorListAPIView(ListAPIView):
	serializer_class = ActorListSerializer
	def get_queryset(self):
		queryset_list = Actor.objects.all()
		return queryset_list

class ActorDetailAPIView(RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
    lookup_field = 'slug'
