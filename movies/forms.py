from django import forms
from .models import Movie, MovieComment, MovieCategory
from multiselectfield import MultiSelectField

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

class MovieCategoryForm(forms.Form):
	category = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=CATEGORIES))

	def clean_category(self, *args, **kwargs):
		category = self.cleaned_data['category']
		category = ''.join(category.split())
		category = ''.join(category.replace("'", ""))
		category = category[1:-1]
		category_list = category.split(",")
		if len(category_list) > 3:
			raise forms.ValidationError("Select up to 3 categories")
		return category_list







