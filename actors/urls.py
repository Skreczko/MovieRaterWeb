
from django.urls import path
from .views import ActorListView, ActorDetailView

urlpatterns = [

	path('', ActorListView.as_view(), name='actor_list'),
	path('<slug>', ActorDetailView.as_view(), name='actor_detail'),


]