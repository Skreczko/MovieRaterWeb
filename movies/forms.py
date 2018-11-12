from django import forms
from .models import Movie, MovieComment





class MovieForm(forms.ModelForm):
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
	category = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=CATEGORIES))

	class Meta:
		model = Movie
		fields = [
			'title',
			'year_of_production',
			'category',
			'production',
			'budget',
			'poster',
			'duration',
			'description',
		]

		widgets = {
			'year_of_production': forms.Select,
			'duration': forms.Select,
		}


class MovieCommentForm(forms.ModelForm):

	class Meta:
		model = MovieComment
		fields = ['movie', 'comment', 'stars']

