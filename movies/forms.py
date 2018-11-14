from django import forms
from .models import Movie, MovieComment, MovieCategory

from .models import CATEGORIES, YEARS, DURATION




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

class MovieCategoryForm(forms.ModelForm):
	category = forms.CharField(max_length=100, widget=forms.Select(choices=CATEGORIES))
	class Meta:
		model = MovieCategory
		fields = ['category']






