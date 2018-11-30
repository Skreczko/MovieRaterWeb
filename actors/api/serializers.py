
from actors.models import Actor, ActorComment, ActorRole
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField
    )






class ActorListSerializer(ModelSerializer):
	class Meta:
		model = Actor
		fields = (
			'id',
			'name',
			'last_name',
			'original_name',
			'born',
			'actor_age',
			'died',
			'average_stars',
			'photo',
		)


class ActorCommentSerializer(ModelSerializer):
	class Meta:
		model = ActorComment
		fields = (
			'id',
			'stars',
			'publish_date',
			'edited_date',
			'added_time',
			'edited_time',
			'comment',
		)


actor_detail_url = HyperlinkedIdentityField(
        view_name='actors-api:detail',
        lookup_field='slug'
        )

class ActorDetailSerializer(ModelSerializer):
	url = actor_detail_url
	actor_comment = ActorCommentSerializer(many=True)
	class Meta:
		model = Actor
		fields = (
			'url',
			'html',
			'id',
			'name',
			'last_name',
			'original_name',
			'born',
			'actor_age',
			'died',
			'average_stars',
			'photo',
			'city_of_birth',
			'nationality',
			'biography',
			'actor_comment',
		)

