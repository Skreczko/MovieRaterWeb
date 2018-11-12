from django import forms
from .models import Movie, MovieComment


YEARS = ((x,x) for x in range(1930,2041))
DURATION = ((x,x) for x in range(0,720))


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
	year_of_production = forms.IntegerField(widget=forms.Select(choices=YEARS))
	duration = forms.IntegerField(widget=forms.Select(choices=DURATION), help_text="in minutes")
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


class MovieCommentForm(forms.ModelForm):

	class Meta:
		model = MovieComment
		fields = ['movie', 'comment', 'stars']

