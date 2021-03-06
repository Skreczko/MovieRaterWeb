from django import forms
from .models import Movie, MovieComment, MovieGallery
from decimal import Decimal

from .models import CATEGORIES, YEARS, DURATION




class MovieForm(forms.ModelForm):
	description = forms.CharField(max_length=295, help_text="295 character maximum.",
								  widget=forms.Textarea(attrs={'rows':5, 'cols':10}))
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
			'description': forms.Textarea(attrs={"rows":10, "cols":10}),

		}

		def clean_description(self, *args, **kwargs):
			description = self.cleaned_data.get('description')
			if len(description) > 295:
				raise forms.ValidationError("The maximum number "
											"of characters has been exceeded by {}.".format(len(description)))
			return description




class MovieCommentForm(forms.ModelForm):
	class Meta:
		model = MovieComment
		fields = ['comment', 'stars']

		widgets = {
			'comment': forms.Textarea

		}

class MovieStarsForm(forms.Form):
	stars = forms.IntegerField()


class MovieCategoryForm(forms.Form):
	category = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=CATEGORIES), label="Maximum of categories per movie is 3.")

	def clean_category(self, *args, **kwargs):

		category = self.cleaned_data['category']
		print (category)
		category = ''.join(category.split())
		category = ''.join(category.replace("'", ""))
		category = category[1:-1]
		category_list = category.split(",")
		if len(category_list) > 3:
			raise forms.ValidationError("Maximum of categories per movie is 3.")
		print(category_list)
		print (category)
		return category_list


class MovieGalleryForm(forms.ModelForm):
	class Meta:
		model = MovieGallery
		fields = ['picture']









