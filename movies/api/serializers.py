
from movies.models import Movie, MovieCategory
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
			''
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

