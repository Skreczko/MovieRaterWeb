
from actors.models import Actor, ActorRole
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField
    )




class ActorRoleSerializer(ModelSerializer):
	class Meta:
		model = ActorRole
		fields = [
			'id',
			'actor',
			'role',
		]

class MovieListSerializer(ModelSerializer):
	movie_category = CategorySerializer(many=True)

	class Meta:
		model = Movie
		fields = (