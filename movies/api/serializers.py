
from movies.models import Movie, MovieCategory, MovieGallery
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField
    )



class CategorySerializer(ModelSerializer):
	class Meta:
		model = MovieCategory
		fields = [
			'id',
			'category',
		]


class MovieListSerializer(ModelSerializer):
	movie_category = CategorySerializer(many=True)

	class Meta:
		model = Movie
		fields = (
			'id',
			'title',
			'year_of_production',
			'duration',
			'movie_category',
			'average_stars',

			'production',
			'budget',
			'poster',
			'description',

		)


class MovieGallerySerializer(ModelSerializer):
	class Meta:
		model = MovieGallery
		fields = (
			'id',
			'picture',
		)



class MovieCommentsSerializer(ModelSerializer):
	class Meta:
		model = Movie
		fields = (
			'id',
			'stars',
			'publish_date',
			'added_time',
			'edited_date',
			'edited_time',
			'comment',
			'added_by',
		)

movie_detail_url = HyperlinkedIdentityField(
        view_name='movies-api:detail',
        lookup_field='slug'
        )

class MovieDetailSerializer(ModelSerializer):
	url = movie_detail_url
	movie_category = CategorySerializer(many=True)
	movie_gallery = MovieGallerySerializer(many=True)

	class Meta:
		model = Movie
		fields = (
			'id',
			'title',
			'year_of_production',
			'duration',
			'movie_category',
			'average_stars',
			'production',
			'budget',
			'poster',
			'description',

		)


# class MovieListSerializer(ModelSerializer):
# 	cat = CategorySerializer(many=True)
#     class Meta:
#         model = Movie
#         fields = ('id',
# 				  'title',
# 				  'year_of_production',
# 				  'duration',
# 				  'cat',
# 				  'production',
# 				  'budget',
# 				  'poster',
# 				  'description',
# 				  'average_stars',
# 				  )


# class CommentSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = MovieComment
# 		fields = ('id', 'comment', 'stars', 'publish_date', 'edited_date', )
#
#
#
#
#
# class MovieListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         fields = ('id', 'title', 'slug', 'year_of_production',
# 				  'production', 'budget', 'poster', 'duration', 'description','average_stars')
#

