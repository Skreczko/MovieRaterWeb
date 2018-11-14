from django import forms
from .models import Movie, MovieComment, MovieCategory

YEARS = ((x, x) for x in range(1930, 2041))
DURATION = ((x, x) for x in range(0, 721))
CATEGORIES = (
	('Action', 'Action'),
	('Adventure', 'Adventure'),
	('Animation', 'Animation'),
	('Anime', 'Anime'),
	('Biography', 'Biography'),
	('Comedy', 'Comedy'),
	('Crime', 'Crime'),
	('Documentary', 'Documentary'),
	('Drama', 'Drama'),
	('Family', 'Family'),
	('Fantasy', 'Fantasy'),
	('Film - Noir', 'Film-Noir'),
	('History', 'History'),
	('Horror', 'Horror'),
	('Musical', 'Musical'),
	('Romence', 'Romence'),
	('Sci - Fi', 'Sci-Fi'),
	('Thriller', 'Thriller'),
	('War', 'War'),
	('Western', 'Western'),
)

class MovieForm(forms.ModelForm):

	class Meta:
		model = Movie
		fields = [
			'title',
			'year_of_production',
			'production',
			'budget',
			'poster',
			'duration',
			'description',
		]

		widgets = {
			'year_of_production': forms.Select(choices=YEARS),
			'duration': forms.Select(choices=DURATION),
		}


class MovieCommentForm(forms.ModelForm):

	class Meta:
		model = MovieComment
		fields = ['movie', 'comment', 'stars']

class MovieCategoryForm(forms.Form):
	category = forms.CharField(max_length=100, widget=forms.Select(choices=CATEGORIES))
	class Meta:
		model = MovieCategory
		fields = ['category', 'related_movie']

class MovieCategoryFormAdmin(forms.ModelForm):
	category = forms.CharField(max_length=100, widget=forms.Select(choices=CATEGORIES))
	class Meta:
		model = MovieCategory
		fields = ['category', 'related_movie']






